import logging
import os
import time
from typing import Optional

from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import APIError

from .prompts import build_voice_companion_prompt

load_dotenv()

logger = logging.getLogger(__name__)

DEFAULT_MODEL = "gemini-3.6-flash"
MAX_RETRIES = 3
BASE_RETRY_DELAY = 2  # seconds; doubles each retry (2s, 4s, 8s)


class LLMClient:
    """Generate dementia-friendly responses using the Gemini API."""

    def __init__(
        self,
        model: str = DEFAULT_MODEL,
        api_key: Optional[str] = None,
        system_prompt: Optional[str] = None,
        temperature: float = 0.6,
        max_retries: int = MAX_RETRIES,
    ):
        api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set. Check your .env file.")

        self.model = model
        # Falls back to the default voice-companion prompt (English,
        # general_conversation intent, no extra context) if none is given.
        # Callers that know the language/intent/context (e.g.
        # ConversationManager) should build their own prompt with
        # build_voice_companion_prompt() and pass it into generate_response().
        self.system_prompt = system_prompt or build_voice_companion_prompt()
        self.temperature = temperature
        self.max_retries = max_retries
        self.client = genai.Client(api_key=api_key)

    def generate_response(
        self,
        user_text: str,
        system_prompt: Optional[str] = None,
    ) -> str:
        """
        Generate an AI response from the patient's text.

        Args:
            user_text: Text received from speech-to-text.
            system_prompt: Optional override for this call's instructions.
                Typically built via prompts.build_voice_companion_prompt()
                with the correct language/intent/context. Falls back to
                the instance's default system_prompt if not provided.

        Returns:
            AI-generated response text.

        Raises:
            ValueError: If user_text is empty.
            RuntimeError: If the API call fails after all retries, or returns nothing.
        """
        if not user_text or not user_text.strip():
            raise ValueError("user_text cannot be empty.")

        active_system_prompt = system_prompt or self.system_prompt

        logger.info("Generating LLM response using model=%s", self.model)

        response = None
        last_error: Optional[APIError] = None

        for attempt in range(1, self.max_retries + 1):
            try:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=user_text.strip(),
                    config=types.GenerateContentConfig(
                        system_instruction=active_system_prompt,
                        temperature=self.temperature,
                    ),
                )
                break
            except APIError as exc:
                last_error = exc
                is_last_attempt = attempt == self.max_retries

                if is_last_attempt:
                    logger.exception(
                        "LLM request failed after %d attempts", self.max_retries
                    )
                    raise RuntimeError(f"LLM request failed: {exc}") from exc

                wait_seconds = BASE_RETRY_DELAY * (2 ** (attempt - 1))
                logger.warning(
                    "LLM request attempt %d/%d failed (%s). Retrying in %ds...",
                    attempt,
                    self.max_retries,
                    exc,
                    wait_seconds,
                )
                time.sleep(wait_seconds)

        response_text = (response.text or "").strip() if response else ""
        if not response_text:
            raise RuntimeError("LLM returned an empty response.")

        return response_text


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    llm = LLMClient()

    try:
        user_text = input("Patient: ")
        result = llm.generate_response(user_text)
        print("\nAI Companion:")
        print(result)
    except (ValueError, RuntimeError) as err:
        print(f"Error: {err}")