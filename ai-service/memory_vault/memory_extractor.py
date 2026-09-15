"""
Memory Extractor

Takes a patient's personal memory/story and extracts:
- people
- places
- events
- dates
- objects
- emotions
- summary
"""

import json
import logging
import os
import time
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import APIError

load_dotenv()

logger = logging.getLogger(__name__)

DEFAULT_MODEL = "gemini-3.6-flash"
MAX_RETRIES = 3
BASE_RETRY_DELAY = 2  # seconds; doubles each retry (2s, 4s, 8s)

MEMORY_EXTRACTION_PROMPT = """You are a memory extraction assistant for a dementia care application.

Your task is to analyze a patient's personal memory or story and
extract important information from it.

Extract:

1. people
   - Name of the person
   - Relationship to the patient if mentioned

2. places
   - Cities
   - Villages
   - Homes
   - Schools
   - Workplaces
   - Other meaningful locations

3. events
   - Important events or activities mentioned in the memory

4. dates
   - Exact dates if mentioned
   - Years
   - Months
   - Approximate time periods

5. objects
   - Important objects mentioned in the memory

6. emotions
   - Feelings or emotions expressed in the memory

7. summary
   - A short and simple summary of the memory

IMPORTANT:
- Do not invent information.
- Only extract information that is present in the story.
- If something is not mentioned, return an empty list.
- Keep the summary concise.
- Preserve the patient's meaning.

Return ONLY valid JSON in exactly this format:

{
  "people": [
    {
      "name": "string",
      "relationship": "string"
    }
  ],
  "places": ["string"],
  "events": ["string"],
  "dates": ["string"],
  "objects": ["string"],
  "emotions": ["string"],
  "summary": "string"
}""".strip()


class MemoryExtractor:
    """Extract structured information from a patient's memory."""

    def __init__(
        self,
        model: str = DEFAULT_MODEL,
        api_key: Optional[str] = None,
        max_retries: int = MAX_RETRIES,
    ):
        """
        Initialize the Memory Extractor.

        API key is read from GEMINI_API_KEY in .env
        if it is not provided directly.
        """
        self.model = model
        self.max_retries = max_retries

        self.api_key = api_key or os.getenv("GEMINI_API_KEY")

        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is not set. Add it to your .env file.")

        self.client = genai.Client(api_key=self.api_key)

    # ---------------------------------------------------------
    # Extract memory
    # ---------------------------------------------------------

    def extract_memory(self, story_text: str) -> Dict[str, Any]:
        """
        Extract structured information from a memory/story.

        Args:
            story_text: Patient's memory or story.

        Returns:
            Dictionary containing extracted memory information.

        Raises:
            ValueError: If story_text is empty.
            RuntimeError: If the API call fails after retries, or
                returns invalid/unusable data.
        """
        if not story_text or not story_text.strip():
            raise ValueError("story_text cannot be empty")

        response_text = self._call_with_retries(story_text.strip())
        result = self._parse_response(response_text)

        logger.info(
            "Memory extracted: %d people, %d places, %d events",
            len(result["people"]),
            len(result["places"]),
            len(result["events"]),
        )

        return result

    # ---------------------------------------------------------
    # API call with retry
    # ---------------------------------------------------------

    def _call_with_retries(self, story_text: str) -> str:
        """Call Gemini with retry on transient API errors."""
        last_error: Optional[APIError] = None

        for attempt in range(1, self.max_retries + 1):
            try:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=story_text,
                    config=types.GenerateContentConfig(
                        system_instruction=MEMORY_EXTRACTION_PROMPT,
                        temperature=0.2,
                        response_mime_type="application/json",
                    ),
                )

                response_text = (response.text or "").strip()
                if not response_text:
                    raise RuntimeError("Gemini returned an empty response.")

                return response_text

            except APIError as exc:
                last_error = exc
                is_last_attempt = attempt == self.max_retries

                if is_last_attempt:
                    logger.exception(
                        "Memory extraction failed after %d attempts", self.max_retries
                    )
                    raise RuntimeError(f"Memory extraction failed: {exc}") from exc

                wait_seconds = BASE_RETRY_DELAY * (2 ** (attempt - 1))
                logger.warning(
                    "Extraction attempt %d/%d failed (%s). Retrying in %ds...",
                    attempt,
                    self.max_retries,
                    exc,
                    wait_seconds,
                )
                time.sleep(wait_seconds)

        # Unreachable in practice, but keeps type-checkers happy
        raise RuntimeError(f"Memory extraction failed: {last_error}")

    # ---------------------------------------------------------
    # Parse JSON
    # ---------------------------------------------------------

    def _parse_response(self, response_text: str) -> Dict[str, Any]:
        """Parse and validate Gemini's JSON response."""
        try:
            data = json.loads(response_text)
        except json.JSONDecodeError as exc:
            logger.error("Invalid JSON returned by Gemini: %s", response_text)
            raise RuntimeError("Gemini returned invalid JSON.") from exc

        return self._validate_result(data)

    # ---------------------------------------------------------
    # Validate result
    # ---------------------------------------------------------

    def _validate_result(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Ensure the response has the expected structure."""
        if not isinstance(data, dict):
            raise ValueError("Memory extraction result must be a JSON object.")

        result = {
            "people": self._validate_people(data.get("people", [])),
            "places": self._validate_string_list(data.get("places", [])),
            "events": self._validate_string_list(data.get("events", [])),
            "dates": self._validate_string_list(data.get("dates", [])),
            "objects": self._validate_string_list(data.get("objects", [])),
            "emotions": self._validate_string_list(data.get("emotions", [])),
            "summary": data.get("summary", ""),
        }

        if not isinstance(result["summary"], str):
            result["summary"] = ""

        return result

    @staticmethod
    def _validate_string_list(value: Any) -> List[str]:
        """Coerce a field into a list of strings, dropping anything malformed."""
        if not isinstance(value, list):
            return []
        return [str(item).strip() for item in value if str(item).strip()]

    @staticmethod
    def _validate_people(value: Any) -> List[Dict[str, str]]:
        """
        Ensure each person entry is a well-formed
        {"name": str, "relationship": str} dict.

        Malformed entries (wrong type, missing name) are dropped rather
        than raising, so one bad item doesn't fail the whole extraction —
        but downstream code (e.g. memory_graph) can then safely assume
        every entry here has both keys.
        """
        if not isinstance(value, list):
            return []

        validated = []
        for item in value:
            if isinstance(item, dict) and item.get("name"):
                validated.append(
                    {
                        "name": str(item.get("name", "")).strip(),
                        "relationship": str(item.get("relationship", "")).strip(),
                    }
                )
            elif isinstance(item, str) and item.strip():
                # Gemini occasionally returns plain strings instead of
                # objects despite the prompt — salvage the name at least.
                validated.append({"name": item.strip(), "relationship": ""})

        return validated


# ---------------------------------------------------------
# Simple test
# ---------------------------------------------------------

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    extractor = MemoryExtractor()

    story = """
    When I was young, I lived in Shillong with my brother Ramesh.
    Every Sunday we went to Ward's Lake. I remember carrying
    my blue school bag. Those days made me very happy.
    """

    result = extractor.extract_memory(story)

    result = extractor.extract_memory(story)

    result = extractor.extract_memory(story)

    print("\nExtracted Memory:")
    print(json.dumps(result, indent=2, ensure_ascii=False))