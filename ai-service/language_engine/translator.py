"""
Translator

Translates text between the 7 supported languages.

Routing logic:
- If both source and target languages are Gemini-handled (en, hi, bn),
  translation goes through Gemini directly — this is reliable.
- If either language is a Bhashini-handled regional language (as, ml,
  mni, brx), translation SHOULD go through Bhashini instead, since it's
  purpose-built for these languages and Gemini's own support for some
  of them (Bodo especially) is weak or unconfirmed (see language_config.py
  and language_detector.py for the reasoning already established there).

IMPORTANT — current status:
The Bhashini translation client is not yet implemented (BhashiniClient
below is a placeholder — see personalized_voice/voice_service.py for
the same "not connected yet" pattern used elsewhere in this project).
Until it's wired in, any translation involving a regional language
falls back to attempting it via Gemini, but the result is explicitly
marked confidence="low" so callers know not to trust it blindly —
this mirrors the same honesty principle used in language_detector.py
rather than silently pretending Gemini handles these languages well.
"""

import logging
import os
import time
from typing import Dict, Optional

import requests
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import APIError

from .language_config import get_language_name, get_provider, is_supported, PROVIDER_REGIONAL_API

load_dotenv()

logger = logging.getLogger(__name__)

DEFAULT_MODEL = "gemini-3.6-flash"
MAX_RETRIES = 3
BASE_RETRY_DELAY = 2  # seconds; doubles each retry (2s, 4s, 8s)

TRANSLATION_PROMPT_TEMPLATE = """Translate the following text from {source_name} to {target_name}.

Return ONLY the translated text, with no explanations, notes, or quotation marks.

Text:
{text}"""


class BhashiniClient:
    """
    Real client for Bhashini's translation service.

    Bhashini uses a two-step call pattern:
    1. POST to the ULCA auth endpoint with your userID/ulcaApiKey to fetch
       the pipeline config for the requested language pair. The response
       includes a serviceId AND a fresh inferenceApiKey for step 2.
    2. POST to the actual Dhruva inference endpoint, using that
       inferenceApiKey, to run the translation itself.

    Pipeline configs are cached per (source_language, target_language)
    pair for the lifetime of this client instance, since step 1 doesn't
    need to be repeated for every single translation call — only once
    per language pair (or if the cached inferenceApiKey stops working,
    in which case a fresh fetch is retried once).
    """

    ULCA_AUTH_URL = "https://meity-auth.ulcacontrib.org/ulca/apis/v0/model/getModelsPipeline"
    INFERENCE_URL = "https://dhruva-api.bhashini.gov.in/services/inference/pipeline"
    # Generic translation pipeline ID used across Bhashini integrations
    # (confirm this is still current in Bhashini's docs/dashboard if
    # translation requests start failing with a pipeline-not-found error).
    PIPELINE_ID = "64392f96daac500b55c543cd"

    REQUEST_TIMEOUT_SECONDS = 60
    # Inference calls specifically (not pipeline config fetches) get a
    # separate, longer timeout, since Bhashini can take significantly
    # longer to respond on the FIRST call for a less-common language
    # pair — likely a model cold-start on their infrastructure. This
    # has been observed to occasionally exceed even 20-30 seconds for
    # regional-language pairs like English->Bodo.
    INFERENCE_TIMEOUT_SECONDS = 60

    def __init__(self, user_id: Optional[str] = None, api_key: Optional[str] = None) -> None:
        self.user_id = user_id or os.getenv("BHASHINI_USER_ID")
        self.api_key = api_key or os.getenv("BHASHINI_API_KEY")

        # Cache: (source_language, target_language) -> {"service_id": ..., "inference_api_key": ...}
        self._pipeline_cache: Dict[tuple, Dict[str, str]] = {}

    def is_configured(self) -> bool:
        """Whether Bhashini credentials are present in the environment."""
        return bool(self.user_id and self.api_key)

    # ---------------------------------------------------------
    # Step 1: fetch pipeline config for a language pair
    # ---------------------------------------------------------

    def _get_pipeline_config(self, source_language: str, target_language: str) -> Dict[str, str]:
        """
        Fetch (or return cached) serviceId + inferenceApiKey for this
        language pair's translation pipeline.
        """
        cache_key = (source_language, target_language)
        if cache_key in self._pipeline_cache:
            return self._pipeline_cache[cache_key]

        payload = {
            "pipelineTasks": [
                {
                    "taskType": "translation",
                    "config": {
                        "language": {
                            "sourceLanguage": source_language,
                            "targetLanguage": target_language,
                        }
                    },
                }
            ],
            "pipelineRequestConfig": {"pipelineId": self.PIPELINE_ID},
        }
        headers = {
            "userID": self.user_id,
            "ulcaApiKey": self.api_key,
            "Content-Type": "application/json",
        }

        response = requests.post(
            self.ULCA_AUTH_URL,
            json=payload,
            headers=headers,
            timeout=self.REQUEST_TIMEOUT_SECONDS,
        )
        try:
            response.raise_for_status()
        except requests.HTTPError as exc:
            raise RuntimeError(
                f"Bhashini API returned {response.status_code}: {response.text}"
            ) from exc
        data = response.json()

        try:
            service_id = data["pipelineResponseConfig"][0]["config"][0]["serviceId"]
            # Keep the FULL language object from Bhashini's response as-is —
            # it includes sourceScriptCode/targetScriptCode alongside the
            # language codes, which the inference call actually requires.
            # Manually rebuilding a stripped-down version (just
            # sourceLanguage/targetLanguage) causes a DHRUVA-101
            # "Failed to send request" error at inference time.
            language_config = data["pipelineResponseConfig"][0]["config"][0]["language"]
            inference_key_info = data["pipelineInferenceAPIEndPoint"]["inferenceApiKey"]
            inference_api_key_name = inference_key_info["name"]
            inference_api_key_value = inference_key_info["value"]
            callback_url = data["pipelineInferenceAPIEndPoint"]["callbackUrl"]
        except (KeyError, IndexError, TypeError) as exc:
            raise RuntimeError(
                f"Unexpected pipeline config response shape from Bhashini: {data}"
            ) from exc

        config = {
            "service_id": service_id,
            "language_config": language_config,
            "inference_api_key_name": inference_api_key_name,
            "inference_api_key_value": inference_api_key_value,
            "callback_url": callback_url,
        }
        self._pipeline_cache[cache_key] = config
        return config

    # ---------------------------------------------------------
    # Step 2: run the actual translation
    # ---------------------------------------------------------

    def translate(self, text: str, source_language: str, target_language: str) -> str:
        """
        Translate text via Bhashini. Retries the inference call once on
        a timeout, since Bhashini's first call for a less-common
        language pair can be slow (likely a model cold-start) even
        when subsequent calls are fast.

        Raises:
            RuntimeError: If credentials are missing, the pipeline config
                can't be fetched, or the inference call fails after retry.
        """
        if not self.is_configured():
            raise RuntimeError(
                "Bhashini credentials are not configured "
                "(set BHASHINI_USER_ID and BHASHINI_API_KEY in .env)."
            )

        config = self._get_pipeline_config(source_language, target_language)

        payload = {
            "pipelineTasks": [
                {
                    "taskType": "translation",
                    "config": {
                        "language": config["language_config"],
                        "serviceId": config["service_id"],
                    },
                }
            ],
            "inputData": {"input": [{"source": text}]},
        }
        headers = {
            "Content-Type": "application/json",
            config["inference_api_key_name"]: config["inference_api_key_value"],
        }

        last_error: Optional[Exception] = None
        for attempt in (1, 2):
            try:
                response = requests.post(
                    config["callback_url"],
                    json=payload,
                    headers=headers,
                    timeout=self.INFERENCE_TIMEOUT_SECONDS,
                )
                break
            except requests.Timeout as exc:
                last_error = exc
                if attempt == 1:
                    logger.warning(
                        "Bhashini inference call timed out on first attempt "
                        "(possible cold-start for %s -> %s); retrying once.",
                        source_language,
                        target_language,
                    )
                    continue
                raise RuntimeError(
                    f"Bhashini inference call timed out twice: {exc}"
                ) from exc
        else:
            raise RuntimeError(f"Bhashini inference call timed out twice: {last_error}")

        try:
            response.raise_for_status()
        except requests.HTTPError as exc:
            raise RuntimeError(
                f"Bhashini API returned {response.status_code}: {response.text}"
            ) from exc
        data = response.json()

        try:
            translated_text = data["pipelineResponse"][0]["output"][0]["target"]
        except (KeyError, IndexError, TypeError) as exc:
            raise RuntimeError(
                f"Unexpected inference response shape from Bhashini: {data}"
            ) from exc

        return translated_text


class Translator:
    """Translates text between the 7 supported languages."""

    def __init__(
        self,
        model: str = DEFAULT_MODEL,
        api_key: Optional[str] = None,
        max_retries: int = MAX_RETRIES,
        bhashini_client: Optional[BhashiniClient] = None,
    ) -> None:
        self.model = model
        self.max_retries = max_retries

        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is not set. Add it to your .env file.")

        self.client = genai.Client(api_key=self.api_key)
        self.bhashini_client = bhashini_client or BhashiniClient()

    # ---------------------------------------------------------
    # Main entry point
    # ---------------------------------------------------------

    def translate(
        self,
        text: str,
        source_language: str,
        target_language: str,
    ) -> Dict[str, str]:
        """
        Translate text from source_language to target_language.

        Args:
            text: The text to translate.
            source_language: Language code the text is currently in.
            target_language: Language code to translate the text into.

        Returns:
            {
                "translated_text": str,
                "confidence": "high" | "low",
                "method": "no_translation_needed" | "gemini" | "bhashini",
            }

        Raises:
            ValueError: If text is empty, or either language code is
                not one of the 7 supported languages.
            RuntimeError: If the translation call fails after retries.
        """
        if not text or not text.strip():
            raise ValueError("text cannot be empty.")

        if not is_supported(source_language):
            raise ValueError(f"source_language '{source_language}' is not supported.")

        if not is_supported(target_language):
            raise ValueError(f"target_language '{target_language}' is not supported.")

        if source_language == target_language:
            return {
                "translated_text": text,
                "confidence": "high",
                "method": "no_translation_needed",
            }

        involves_regional_language = (
            get_provider(source_language) == PROVIDER_REGIONAL_API
            or get_provider(target_language) == PROVIDER_REGIONAL_API
        )

        if involves_regional_language:
            return self._translate_regional(text, source_language, target_language)

        return self._translate_with_gemini(text, source_language, target_language)

    # ---------------------------------------------------------
    # Regional-language translation (Bhashini, with Gemini fallback)
    # ---------------------------------------------------------

    def _translate_regional(
        self, text: str, source_language: str, target_language: str
    ) -> Dict[str, str]:
        """
        Attempt translation via Bhashini for a pair involving at least
        one regional language. Falls back to Gemini (marked low
        confidence) if Bhashini isn't configured or the call fails —
        Bhashini should be the primary path once configured, but a
        live API can always fail at runtime (network issues, an
        unsupported language pair, a temporary outage), and a live
        conversation shouldn't crash just because Bhashini had a bad moment.
        """
        if self.bhashini_client.is_configured():
            try:
                translated_text = self.bhashini_client.translate(
                    text, source_language, target_language
                )
                return {
                    "translated_text": translated_text,
                    "confidence": "high",
                    "method": "bhashini",
                }
            except Exception as exc:
                logger.warning(
                    "Bhashini translation failed (%s); falling back to Gemini for "
                    "%s -> %s (low confidence).",
                    exc,
                    source_language,
                    target_language,
                )
        else:
            logger.warning(
                "Bhashini credentials not configured; falling back to Gemini for "
                "%s -> %s (low confidence — Gemini's support for some regional "
                "languages, especially Bodo, is weak or unconfirmed).",
                source_language,
                target_language,
            )

        result = self._translate_with_gemini(text, source_language, target_language)
        result["confidence"] = "low"
        return result

    # ---------------------------------------------------------
    # Gemini-based translation
    # ---------------------------------------------------------

    def _translate_with_gemini(
        self, text: str, source_language: str, target_language: str
    ) -> Dict[str, str]:
        """Translate using Gemini. Reliable for en/hi/bn pairs."""
        prompt = TRANSLATION_PROMPT_TEMPLATE.format(
            source_name=get_language_name(source_language),
            target_name=get_language_name(target_language),
            text=text.strip(),
        )

        translated_text = self._call_with_retries(prompt)

        return {
            "translated_text": translated_text,
            "confidence": "high",
            "method": "gemini",
        }

    def _call_with_retries(self, prompt: str) -> str:
        """Call Gemini with retry on transient API errors."""
        last_error: Optional[APIError] = None

        for attempt in range(1, self.max_retries + 1):
            try:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt,
                    config=types.GenerateContentConfig(temperature=0.2),
                )
                response_text = (response.text or "").strip()
                if not response_text:
                    raise RuntimeError("Gemini returned an empty response.")
                return response_text

            except APIError as exc:
                last_error = exc
                is_last_attempt = attempt == self.max_retries

                if is_last_attempt:
                    logger.exception("Translation failed after %d attempts", self.max_retries)
                    raise RuntimeError(f"Translation failed: {exc}") from exc

                wait_seconds = BASE_RETRY_DELAY * (2 ** (attempt - 1))
                logger.warning(
                    "Translation attempt %d/%d failed (%s). Retrying in %ds...",
                    attempt,
                    self.max_retries,
                    exc,
                    wait_seconds,
                )
                time.sleep(wait_seconds)

        raise RuntimeError(f"Translation failed: {last_error}")


# ---------------------------------------------------------
# Simple test
# ---------------------------------------------------------

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    translator = Translator()

    print("=" * 60)
    print("Gemini-handled pair (English -> Hindi)")
    print("=" * 60)
    result = translator.translate("How are you feeling today?", "en", "hi")
    print(result)

    print("\n" + "=" * 60)
    print("Same language (no-op)")
    print("=" * 60)
    result = translator.translate("Hello", "en", "en")
    print(result)

    print("\n" + "=" * 60)
    print("Regional language pair (English -> Bodo)")
    print("=" * 60)
    result = translator.translate("How are you feeling today?", "en", "brx")
    print(result)

    print("\n" + "=" * 60)
    print("Regional language pair (English -> Malayalam) — better-resourced, isolates whether the issue is Bodo-specific")
    print("=" * 60)
    result = translator.translate("How are you feeling today?", "en", "ml")
    print(result)