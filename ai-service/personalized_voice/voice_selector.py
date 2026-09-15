"""
Voice Selector

Chooses which voice (personalized family voice, or the default AI
voice) should be used to speak a response, given a patient and the
conversation's current language.

Depends on:
    - voice_profile.py (VoiceProfileManager, VoiceProfile)
    - voice_service.py (PersonalizedVoiceService)
    - language_engine/language_config.py (for validating language codes)

Selection logic (in priority order):
    1. If the patient has a personalized voice AND it's ready
       (see PersonalizedVoiceService.is_ready()) AND it matches the
       requested language -> use it.
    2. Otherwise -> fall back to the default AI voice for that language.

This matters specifically because a personalized voice (e.g. a
caregiver's cloned voice) is usually recorded in ONE language. A
patient's conversation might happen in a different language than that
recording (e.g. the family recorded English samples, but today's
conversation is in Bodo) — in that case, using the personalized voice
would be misleading (it wouldn't actually sound like that person
speaking that language), so falling back to the default AI voice for
that language is the correct, honest choice, not a bug.
"""

import logging
from typing import Optional

from language_engine.language_config import is_supported

from .voice_profile import VoiceProfile, VoiceProfileManager
from .voice_service import PersonalizedVoiceService

logger = logging.getLogger(__name__)

DEFAULT_VOICE_ID = "default_voice"


class VoiceSelector:
    """
    Selects the appropriate voice for a patient's response, given the
    conversation's language.
    """

    def __init__(
        self,
        voice_profile_manager: Optional[VoiceProfileManager] = None,
        default_voice_id: str = DEFAULT_VOICE_ID,
    ) -> None:
        self.voice_profile_manager = voice_profile_manager or VoiceProfileManager()
        self.default_voice_id = default_voice_id

        # Ensure a default voice profile always exists, so selection
        # never has "nothing to fall back to" as a failure mode.
        if self.default_voice_id not in self.voice_profile_manager.voices:
            self.voice_profile_manager.add_voice(
                VoiceProfile(
                    voice_id=self.default_voice_id,
                    name="Default AI Voice",
                    provider="gemini",
                    language="en",
                    description="Standard AI companion voice",
                    is_personalized=False,
                    is_available=True,
                )
            )

    # ---------------------------------------------------------
    # Main entry point
    # ---------------------------------------------------------

    def select_voice(
        self,
        language: str,
        personalized_service: Optional[PersonalizedVoiceService] = None,
    ) -> dict:
        """
        Choose which voice to use for a response in `language`.

        Args:
            language: One of the 7 supported language codes.
            personalized_service: The patient's PersonalizedVoiceService,
                if one exists (e.g. built from a caregiver-recorded
                voice). Pass None if the patient has no personalized
                voice set up at all.

        Returns:
            {
                "voice_id": str,
                "is_personalized": bool,
                "reason": str,   # human-readable explanation of the choice,
                                 # useful for logging/debugging voice selection
            }

        Raises:
            ValueError: If language is not one of the 7 supported codes.
        """
        if not is_supported(language):
            raise ValueError(f"Language '{language}' is not supported.")

        if personalized_service is not None:
            if personalized_service.is_ready(language=language):
                voice_id = personalized_service.get_voice_id()
                logger.info(
                    "Selected personalized voice '%s' for language=%s", voice_id, language
                )
                return {
                    "voice_id": voice_id,
                    "is_personalized": True,
                    "reason": f"Personalized voice is ready and matches language '{language}'.",
                }

            # Personalized voice exists but isn't usable for this
            # language/isn't ready — explain why, for debugging, but
            # still fall through to the default voice below.
            if not personalized_service.supports_language(language):
                reason_detail = (
                    f"Personalized voice is configured for "
                    f"'{personalized_service.get_voice_language()}', not '{language}'."
                )
            else:
                reason_detail = "Personalized voice exists but is not ready yet."

            logger.info(
                "Personalized voice not usable for language=%s (%s); falling back to default.",
                language,
                reason_detail,
            )
        else:
            reason_detail = "No personalized voice is set up for this patient."

        default_voice = self._get_default_voice_for_language(language)

        return {
            "voice_id": default_voice.voice_id,
            "is_personalized": False,
            "reason": f"{reason_detail} Using default AI voice.",
        }

    # ---------------------------------------------------------
    # Default voice lookup
    # ---------------------------------------------------------

    def _get_default_voice_for_language(self, language: str) -> VoiceProfile:
        """
        Return an available default (non-personalized) voice for
        `language`, if one is registered; otherwise fall back to the
        base default voice regardless of its language field, since
        having SOME voice to speak with is better than raising an
        error mid-conversation over a missing language-specific
        default voice entry.
        """
        candidates = [
            voice
            for voice in self.voice_profile_manager.get_available_voices(language=language)
            if not voice.is_personalized
        ]

        if candidates:
            return candidates[0]

        logger.warning(
            "No default voice registered specifically for language=%s; "
            "using the base default voice instead.",
            language,
        )
        return self.voice_profile_manager.voices[self.default_voice_id]


# ---------------------------------------------------------
# Simple test
# ---------------------------------------------------------

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    from .voice_dataset import VoiceDatasetManager, VoiceRecording

    selector = VoiceSelector()

    print("=" * 60)
    print("Case 1 — no personalized voice at all")
    print("=" * 60)
    result = selector.select_voice(language="hi", personalized_service=None)
    print(result)

    print("\n" + "=" * 60)
    print("Case 2 — personalized voice exists, matches language, is ready")
    print("=" * 60)
    family_voice = VoiceProfile(
        voice_id="family_voice_en",
        name="Family Voice",
        provider="custom",
        language="en",
        is_personalized=True,
        is_available=True,
    )
    dataset = VoiceDatasetManager(voice_id="family_voice_en")
    dataset.add_recording(
        VoiceRecording(
            recording_id="r1",
            file_path="recordings/sample.wav",
            duration_seconds=90.0,
            language="en",
        )
    )
    service = PersonalizedVoiceService(voice_profile=family_voice, dataset=dataset)
    result = selector.select_voice(language="en", personalized_service=service)
    print(result)

    print("\n" + "=" * 60)
    print("Case 3 — personalized voice exists, but WRONG language requested")
    print("=" * 60)
    result = selector.select_voice(language="hi", personalized_service=service)
    print(result)