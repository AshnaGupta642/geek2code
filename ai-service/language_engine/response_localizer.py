"""
Response Localizer

Verifies that the AI's generated response is actually written in the
language it was supposed to respond in, and corrects it if not, before
it goes to text_to_speech.py.

Why this exists:
LLMs — including Gemini — don't always follow a "respond in X language"
instruction perfectly, especially for languages they support less well
(as we've already established: Bodo and, to a lesser extent, Manipuri
and Assamese, are weaker/unconfirmed for Gemini). A common failure mode
is the model drifting back to English mid-response, or ignoring the
instruction entirely for a low-resource language. Speaking an English
sentence to a patient who was supposed to hear Bodo is a real, silent
failure that would otherwise go undetected until a person actually
listens to the output.

This module closes that gap: it detects the actual language of the
generated response (reusing language_detector.py) and, if it doesn't
match the intended target language, translates it into the correct
language (reusing translator.py) before it's handed off to TTS.
"""

import logging
from typing import Dict, Optional

from .language_config import get_language_name, is_supported
from .language_detector import LanguageDetector
from .translator import Translator

logger = logging.getLogger(__name__)

# Only auto-correct when the mismatch was detected with high confidence.
# A "low" confidence detection (e.g. an ambiguous script that fell back
# to a guess) isn't a reliable enough signal to justify translating an
# otherwise-correct response — that would risk introducing translation
# errors into text that may have been fine to begin with.
MIN_CONFIDENCE_TO_CORRECT = "high"


class ResponseLocalizer:
    """
    Confirms (and if needed, corrects) that a generated response is
    actually in the intended target language before it's spoken aloud.
    """

    def __init__(
        self,
        detector: Optional[LanguageDetector] = None,
        translator: Optional[Translator] = None,
    ) -> None:
        self.detector = detector or LanguageDetector()
        self.translator = translator or Translator()

    # ---------------------------------------------------------
    # Main entry point
    # ---------------------------------------------------------

    def localize(self, response_text: str, target_language: str) -> Dict[str, object]:
        """
        Verify response_text is in target_language; correct it if not.

        Args:
            response_text: The AI-generated response (from llm_client.py),
                which was supposed to be in target_language.
            target_language: The language code the response was meant
                to be in (e.g. what conversation_manager.py requested).

        Returns:
            {
                "text": str,              # the final text to hand to TTS
                "was_corrected": bool,    # True if a mismatch was fixed
                "detected_language": str, # what language the original text was actually in
                "target_language": str,
                "detection_confidence": "high" | "low",
                "note": str | None,       # set if correction was attempted but failed
            }

        Raises:
            ValueError: If response_text is empty or target_language
                is not one of the 7 supported languages.
        """
        if not response_text or not response_text.strip():
            raise ValueError("response_text cannot be empty.")

        if not is_supported(target_language):
            raise ValueError(f"target_language '{target_language}' is not supported.")

        detection = self.detector.detect_language(response_text)
        detected_language = detection["language_code"]
        detection_confidence = detection["confidence"]

        result: Dict[str, object] = {
            "text": response_text,
            "was_corrected": False,
            "detected_language": detected_language,
            "target_language": target_language,
            "detection_confidence": detection_confidence,
            "note": None,
        }

        if detected_language == target_language:
            return result

        if detection_confidence != MIN_CONFIDENCE_TO_CORRECT:
            logger.info(
                "Response looked like it might not be in %s (detected %s), "
                "but detection confidence was low — leaving response as-is "
                "rather than risking an unnecessary translation.",
                target_language,
                detected_language,
            )
            return result

        logger.warning(
            "AI response was generated in '%s' but should have been in '%s' "
            "(%s). Attempting automatic correction via translation.",
            get_language_name(detected_language),
            get_language_name(target_language),
            target_language,
        )

        try:
            translation = self.translator.translate(
                text=response_text,
                source_language=detected_language,
                target_language=target_language,
            )
            result["text"] = translation["translated_text"]
            result["was_corrected"] = True
            if translation["confidence"] == "low":
                result["note"] = (
                    "Response was auto-corrected to the right language, but the "
                    "correction itself used a lower-confidence translation path."
                )
        except (ValueError, RuntimeError) as exc:
            logger.error(
                "Failed to auto-correct response language (%s -> %s): %s. "
                "Speaking the original, wrong-language response rather than "
                "failing the whole conversation turn.",
                detected_language,
                target_language,
                exc,
            )
            result["note"] = (
                f"Response may be in the wrong language ({get_language_name(detected_language)} "
                f"instead of {get_language_name(target_language)}); automatic correction failed."
            )

        return result


# ---------------------------------------------------------
# Simple test
# ---------------------------------------------------------

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    localizer = ResponseLocalizer()

    print("=" * 60)
    print("Case 1 — response already in the correct language")
    print("=" * 60)
    result = localizer.localize("आप कैसे हैं?", target_language="hi")
    print(result)

    print("\n" + "=" * 60)
    print("Case 2 — LLM drifted to English when Hindi was requested")
    print("=" * 60)
    result = localizer.localize(
        "How are you feeling today?", target_language="hi"
    )
    print(result)
    print(f"\nCorrected: {result['was_corrected']}")
    print(f"Final text: {result['text']}")