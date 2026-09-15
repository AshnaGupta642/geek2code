"""
Language Detector

Detects which of the 7 supported languages a piece of text is written in.

Approach (hybrid, not a single off-the-shelf library):
- Common libraries like `langdetect` are trained on major world languages
  and do NOT reliably support Manipuri, Bodo, or Assamese — Assamese in
  particular gets misdetected as Bengali by most generic detectors since
  they share the same script.
- So detection here is done in stages:
    1. Fast, free, no-API Unicode script-range detection. Some scripts
       map to exactly one supported language (e.g. Malayalam script ->
       Malayalam only), so detection stops there immediately.
    2. For scripts shared by multiple supported languages (Devanagari:
       Hindi vs Bodo; Bengali script: Bengali vs Assamese vs Manipuri/
       Bodo written in Bengali script), Bhashini's dedicated "Text
       Language Detection" API is tried first — it's purpose-built for
       exactly this task across Indian languages, and likely far more
       reliable for Bodo/Manipuri than a general-purpose model.
    3. If Bhashini isn't configured or the call fails, this falls back
       to asking Gemini to disambiguate — reliable for Hindi/Bengali,
       but explicitly marked lower-trust for Bodo given Gemini's
       weak/unconfirmed support there (see language_config.py).

This is a "best effort" detector, not a guarantee — in production, this
should support/confirm an explicit language selection from the app
(e.g. a caregiver-set language), not fully replace it.
"""

import json
import logging
import os
import time
from typing import Dict, List, Optional

import requests
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import APIError

from .language_config import (
    DEFAULT_LANGUAGE_CODE,
    is_supported,
)

load_dotenv()

logger = logging.getLogger(__name__)

DEFAULT_MODEL = "gemini-3.6-flash"
MAX_RETRIES = 3
BASE_RETRY_DELAY = 2  # seconds; doubles each retry (2s, 4s, 8s)

# ---------------------------------------------------------
# Unicode script ranges relevant to the 7 supported languages
# ---------------------------------------------------------
# Devanagari (Hindi, and Bodo when written in Devanagari — Bodo's
# official script since 1975)
_DEVANAGARI_RANGE = (0x0900, 0x097F)
# Bengali script (Bengali, Assamese, and Manipuri when written in
# Bengali script rather than Meitei Mayek)
_BENGALI_SCRIPT_RANGE = (0x0980, 0x09FF)
# Malayalam script — used only by Malayalam among supported languages
_MALAYALAM_RANGE = (0x0D00, 0x0D7F)
# Meitei Mayek — Manipuri's native script, unambiguous when present
_MEITEI_MAYEK_RANGE = (0xABC0, 0xABFF)
# Basic Latin — covers English
_LATIN_RANGE = (0x0041, 0x007A)

# Assamese-specific letters not present in standard Bengali: RA (ৰ)
# and VA (ৱ). Their presence strongly indicates Assamese even though
# the overall script block is shared with Bengali.
_ASSAMESE_MARKER_CHARS = {"\u09F0", "\u09F1"}

# Scripts that map to exactly one supported language — no disambiguation needed.
_UNAMBIGUOUS_SCRIPT_LANGUAGE = {
    "malayalam": "ml",
    "meitei_mayek": "mni",
}

# Scripts shared by more than one supported language — need Gemini to
# disambiguate. Maps script name -> candidate language codes.
#
# Bodo's script history is more complicated than a single official
# script: Devanagari became official in 1975, but Assamese/Bengali
# script and Latin script both remain in real-world use by some Bodo
# writers/communities today (not just historically) — so Bodo is
# included as a candidate under BOTH Devanagari and Bengali script,
# not just Devanagari.
_AMBIGUOUS_SCRIPT_CANDIDATES = {
    "devanagari": ["hi", "brx"],
    "bengali_script": ["bn", "as", "mni", "brx"],
}

# NOTE — known limitation: Bodo can also appear in Latin script, but
# Latin script is treated as an unambiguous "English" fast path below
# (see _detect_dominant_script usage) rather than triggering Gemini
# disambiguation, since the overwhelming majority of Latin-script
# input in this app will genuinely be English, and adding a Gemini
# call to every English message just to rule out romanized Bodo would
# add latency/cost with very little practical benefit. If romanized
# Bodo input becomes a real, common case in practice, this should be
# revisited — e.g. only trigger disambiguation when Bodo is the
# app/patient's declared language AND the script is Latin.

DISAMBIGUATION_PROMPT_TEMPLATE = """You are a language identification assistant.

The following text is written in a script shared by multiple languages.
Identify which ONE of these languages it is written in: {candidates}

Text:
{text}

Return ONLY valid JSON in exactly this format, with no other text:
{{"language_code": "one of: {candidates}", "confidence": "high" or "low"}}"""


class BhashiniLanguageDetector:
    """
    Client for Bhashini's dedicated "Text Language Detection" API —
    purpose-built for identifying Indian languages, including ones
    like Bodo and Manipuri that general-purpose models handle poorly
    or not at all.

    Uses the same two-step pipeline pattern as translator.py's
    BhashiniClient: fetch a pipeline config (serviceId + inferenceApiKey)
    for the "txt-lang-detection" task, then call the inference endpoint.
    """

    ULCA_AUTH_URL = "https://meity-auth.ulcacontrib.org/ulca/apis/v0/model/getModelsPipeline"
    INFERENCE_URL = "https://dhruva-api.bhashini.gov.in/services/inference/pipeline"
    REQUEST_TIMEOUT_SECONDS = 60

    def __init__(self, user_id: Optional[str] = None, api_key: Optional[str] = None) -> None:
        self.user_id = user_id or os.getenv("BHASHINI_USER_ID")
        self.api_key = api_key or os.getenv("BHASHINI_API_KEY")
        self._pipeline_cache: Optional[Dict[str, str]] = None

    def is_configured(self) -> bool:
        """Whether Bhashini credentials are present in the environment."""
        return bool(self.user_id and self.api_key)

    def _get_pipeline_config(self) -> Dict[str, str]:
        """Fetch (or return cached) serviceId + inferenceApiKey for text-language-detection."""
        if self._pipeline_cache is not None:
            return self._pipeline_cache

        payload = {"pipelineTasks": [{"taskType": "txt-lang-detection"}]}
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
            inference_key_info = data["pipelineInferenceAPIEndPoint"]["inferenceApiKey"]
            config = {
                "service_id": service_id,
                "inference_api_key_name": inference_key_info["name"],
                "inference_api_key_value": inference_key_info["value"],
                "callback_url": data["pipelineInferenceAPIEndPoint"]["callbackUrl"],
            }
        except (KeyError, IndexError, TypeError) as exc:
            raise RuntimeError(
                f"Unexpected pipeline config response shape from Bhashini: {data}"
            ) from exc

        self._pipeline_cache = config
        return config

    def detect(self, text: str, candidates: Optional[List[str]] = None) -> Dict[str, str]:
        """
        Detect the language of `text` using Bhashini.

        Args:
            text: The text to identify.
            candidates: Optional list of language codes to narrow the
                result to (used when disambiguating a specific script,
                e.g. ["hi", "brx"]). If Bhashini returns a language
                outside this list, the top candidate is used instead
                and confidence is downgraded.

        Raises:
            RuntimeError: If credentials are missing or the API call fails.
        """
        if not self.is_configured():
            raise RuntimeError(
                "Bhashini credentials are not configured "
                "(set BHASHINI_USER_ID and BHASHINI_API_KEY in .env)."
            )

        config = self._get_pipeline_config()

        payload = {
            "pipelineTasks": [{"taskType": "txt-lang-detection"}],
            "inputData": {"input": [{"source": text}]},
        }
        headers = {
            "Content-Type": "application/json",
            config["inference_api_key_name"]: config["inference_api_key_value"],
        }

        response = requests.post(
            config["callback_url"],
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
            detected_code = data["pipelineResponse"][0]["output"][0]["langPrediction"][0][
                "langCode"
            ]
        except (KeyError, IndexError, TypeError) as exc:
            raise RuntimeError(
                f"Unexpected txt-lang-detection response shape from Bhashini: {data}"
            ) from exc

        confidence = "high"
        if candidates and detected_code not in candidates:
            logger.warning(
                "Bhashini detected '%s', outside expected candidates %s; "
                "using top candidate instead.",
                detected_code,
                candidates,
            )
            detected_code = candidates[0]
            confidence = "low"

        return {"language_code": detected_code, "confidence": confidence}


class LanguageDetector:
    """Detects which supported language a piece of text is written in."""

    def __init__(
        self,
        model: str = DEFAULT_MODEL,
        api_key: Optional[str] = None,
        max_retries: int = MAX_RETRIES,
        bhashini_detector: Optional[BhashiniLanguageDetector] = None,
    ) -> None:
        self.model = model
        self.max_retries = max_retries

        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is not set. Add it to your .env file.")

        self.client = genai.Client(api_key=self.api_key)
        self.bhashini_detector = bhashini_detector or BhashiniLanguageDetector()

    # ---------------------------------------------------------
    # Main entry point
    # ---------------------------------------------------------

    def detect_language(self, text: str) -> Dict[str, str]:
        """
        Detect which supported language the given text is written in.

        Args:
            text: The text to identify (e.g. a speech-to-text transcript).

        Returns:
            {
                "language_code": one of the 7 supported codes,
                "confidence": "high" | "low",
                "method": "script" | "bhashini" | "gemini" | "fallback",
            }
            Falls back to DEFAULT_LANGUAGE_CODE with confidence "low"
            and method "fallback" if the text is empty or no signal
            could be extracted at all — this NEVER raises, since a
            failed detection shouldn't crash a live conversation; the
            caller should treat "low" confidence as "maybe confirm
            with the patient/app instead of trusting this blindly."
        """
        if not text or not text.strip():
            return {
                "language_code": DEFAULT_LANGUAGE_CODE,
                "confidence": "low",
                "method": "fallback",
            }

        script = self._detect_dominant_script(text)

        if script in _UNAMBIGUOUS_SCRIPT_LANGUAGE:
            return {
                "language_code": _UNAMBIGUOUS_SCRIPT_LANGUAGE[script],
                "confidence": "high",
                "method": "script",
            }

        if script == "bengali_script":
            # ৰ (RA) and ৱ (VA) are Assamese-alphabet letters not used in
            # standard Bengali, so their presence is a strong signal for
            # Assamese. This is treated as "high confidence" as a
            # practical heuristic, but it isn't airtight: Bodo was
            # historically written using the Assamese alphabet
            # specifically (not just generic Bengali script), so text
            # from a Bodo writer using that older convention could
            # plausibly also contain these letters. In practice this is
            # a rare edge case — most Bengali-script Bodo writing in
            # circulation today uses Devanagari instead — so this
            # heuristic is kept as-is rather than routing every marker
            # match through Bhashini/Gemini, but it's worth revisiting
            # if Bodo patients using this specific convention turn out
            # to be common.
            if any(ch in text for ch in _ASSAMESE_MARKER_CHARS):
                return {"language_code": "as", "confidence": "high", "method": "script"}

        if script == "latin":
            return {"language_code": "en", "confidence": "high", "method": "script"}

        if script in _AMBIGUOUS_SCRIPT_CANDIDATES:
            candidates = _AMBIGUOUS_SCRIPT_CANDIDATES[script]
            return self._disambiguate(text, candidates, script)

        # No recognizable script signal at all (numbers only, symbols,
        # unsupported script, etc.) — fall back to the default language.
        return {
            "language_code": DEFAULT_LANGUAGE_CODE,
            "confidence": "low",
            "method": "fallback",
        }

    # ---------------------------------------------------------
    # Script detection
    # ---------------------------------------------------------

    @staticmethod
    def _detect_dominant_script(text: str) -> Optional[str]:
        """
        Return the name of the Unicode script block with the most
        characters in the text, among the scripts relevant to the 7
        supported languages. Returns None if no relevant script is found.
        """
        counts = {
            "devanagari": 0,
            "bengali_script": 0,
            "malayalam": 0,
            "meitei_mayek": 0,
            "latin": 0,
        }

        for ch in text:
            code_point = ord(ch)

            if _DEVANAGARI_RANGE[0] <= code_point <= _DEVANAGARI_RANGE[1]:
                counts["devanagari"] += 1
            elif _BENGALI_SCRIPT_RANGE[0] <= code_point <= _BENGALI_SCRIPT_RANGE[1]:
                counts["bengali_script"] += 1
            elif _MALAYALAM_RANGE[0] <= code_point <= _MALAYALAM_RANGE[1]:
                counts["malayalam"] += 1
            elif _MEITEI_MAYEK_RANGE[0] <= code_point <= _MEITEI_MAYEK_RANGE[1]:
                counts["meitei_mayek"] += 1
            elif ch.isalpha() and _LATIN_RANGE[0] <= code_point <= _LATIN_RANGE[1]:
                counts["latin"] += 1

        dominant = max(counts, key=counts.get)
        return dominant if counts[dominant] > 0 else None

    # ---------------------------------------------------------
    # Disambiguation for ambiguous scripts (Bhashini first, Gemini fallback)
    # ---------------------------------------------------------

    def _disambiguate(self, text: str, candidates: List[str], script: str) -> Dict[str, str]:
        """
        Resolve which of `candidates` the text is actually written in,
        when script alone can't decide. Tries Bhashini's dedicated
        text-language-detection API first (more reliable for Bodo/
        Manipuri specifically), falling back to Gemini if Bhashini
        isn't configured or the call fails.
        """
        if self.bhashini_detector.is_configured():
            try:
                result = self.bhashini_detector.detect(text, candidates=candidates)
                return {
                    "language_code": result["language_code"],
                    "confidence": result["confidence"],
                    "method": "bhashini",
                }
            except Exception as exc:
                logger.warning(
                    "Bhashini language detection failed (%s) for script=%s; "
                    "falling back to Gemini.",
                    exc,
                    script,
                )
        else:
            logger.info(
                "Bhashini not configured; using Gemini to disambiguate script=%s.", script
            )

        try:
            return self._disambiguate_with_gemini(text, candidates)
        except RuntimeError:
            logger.warning(
                "Gemini disambiguation also failed for script=%s; falling back to first candidate.",
                script,
            )
            return {
                "language_code": candidates[0],
                "confidence": "low",
                "method": "fallback",
            }

    # ---------------------------------------------------------
    # Gemini-based disambiguation for ambiguous scripts (fallback path)
    # ---------------------------------------------------------

    def _disambiguate_with_gemini(self, text: str, candidates: list) -> Dict[str, str]:
        """
        Ask Gemini to pick which of the candidate languages the text is
        actually written in, when script alone can't decide (e.g.
        Devanagari could be Hindi or Bodo). Used only as a fallback
        when Bhashini isn't configured or fails.
        """
        candidates_str = ", ".join(candidates)
        prompt = DISAMBIGUATION_PROMPT_TEMPLATE.format(
            candidates=candidates_str, text=text.strip()
        )

        response_text = self._call_with_retries(prompt)

        try:
            data = json.loads(response_text)
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"Gemini returned invalid JSON: {response_text}") from exc

        language_code = str(data.get("language_code", "")).strip()
        confidence = str(data.get("confidence", "low")).strip()

        if language_code not in candidates:
            logger.warning(
                "Gemini returned an unexpected language_code '%s' outside candidates %s",
                language_code,
                candidates,
            )
            language_code = candidates[0]
            confidence = "low"

        if confidence not in ("high", "low"):
            confidence = "low"

        return {"language_code": language_code, "confidence": confidence, "method": "gemini"}

    def _call_with_retries(self, prompt: str) -> str:
        """Call Gemini with retry on transient API errors."""
        last_error: Optional[APIError] = None

        for attempt in range(1, self.max_retries + 1):
            try:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        temperature=0.0,
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
                        "Language disambiguation failed after %d attempts", self.max_retries
                    )
                    raise RuntimeError(f"Language disambiguation failed: {exc}") from exc

                wait_seconds = BASE_RETRY_DELAY * (2 ** (attempt - 1))
                logger.warning(
                    "Disambiguation attempt %d/%d failed (%s). Retrying in %ds...",
                    attempt,
                    self.max_retries,
                    exc,
                    wait_seconds,
                )
                time.sleep(wait_seconds)

        raise RuntimeError(f"Language disambiguation failed: {last_error}")


# ---------------------------------------------------------
# Simple test
# ---------------------------------------------------------

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    detector = LanguageDetector()

    test_cases = {
        "English (Latin script)": "Hello, how are you today?",
        "Hindi (Devanagari)": "आज आप कैसे हैं?",
        "Bengali (Bengali script)": "আজ আপনি কেমন আছেন?",
        "Assamese (Bengali script + marker chars)": "মোৰ নাম ৰাম, মই ভাল আছোঁ।",
        "Malayalam (Malayalam script)": "ഇന്ന് സുഖമാണോ?",
        "Manipuri (Meitei Mayek script)": "ꯅꯪꯒꯨꯝ ꯀꯔꯝꯅꯤ",
        "Empty string": "",
    }

    for label, text in test_cases.items():
        result = detector.detect_language(text)
        print(f"{label}:")
        print(f"  Text: {text!r}")
        print(f"  Result: {result}\n")