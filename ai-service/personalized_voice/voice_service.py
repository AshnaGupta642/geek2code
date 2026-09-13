"""
Personalized Voice Service

Connects a selected VoiceProfile with ElevenLabs for real voice
cloning and text-to-speech.

Based on ElevenLabs' confirmed current official API (verified via
their docs/GitHub, not guessed blindly):
    - Cloning: client.voices.ivc.create(name=..., files=[...]) -> voice.voice_id
    - Speech:  client.text_to_speech.convert(text=..., voice_id=..., model_id=...)

NOTE: this has NOT yet been tested against a live ElevenLabs account
(no API key was available at the time this was written) — the shape
matches their documented API closely, but as we learned from Bhashini,
even well-documented APIs can have small live quirks (missing fields,
different validation rules) that only surface on a real test. Test
clone_voice() and generate_speech() against a real account before
fully trusting this in a live conversation.
"""

import logging
import os
from typing import List, Optional

from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs

from personalized_voice.voice_profile import VoiceProfile
from personalized_voice.voice_dataset import VoiceDatasetManager

load_dotenv()

logger = logging.getLogger(__name__)

DEFAULT_MODEL_ID = "eleven_v3"  # broader language coverage than eleven_multilingual_v2
DEFAULT_OUTPUT_FORMAT = "mp3_44100_128"  # ElevenLabs' default; output is .mp3, not .wav

# CONFIRMED (via ElevenLabs' own docs) language coverage relevant to this
# project's 7 supported languages:
#   - eleven_multilingual_v2 (29 languages): covers en, hi — NOT bn/as/ml
#   - eleven_v3 (70+ languages): covers en, hi, bn, as, ml
#   - NEITHER model lists Manipuri (mni) or Bodo (brx) as supported —
#     these are extremely low-resource languages that ElevenLabs
#     doesn't appear to cover at all, similar to the Gemini gap found
#     earlier for these same two languages.
# Practical implication: a personalized/cloned voice can only be used
# for en/hi/bn/as/ml. For mni/brx, PersonalizedVoiceService.is_ready()
# and supports_language() will correctly return False for these codes
# via the ELEVENLABS_UNSUPPORTED_LANGUAGES check below, and callers
# (e.g. voice_selector.py) should fall back to the default AI voice
# (Gemini/Bhashini pipeline) for those two languages — not attempt
# personalized cloning at all.
ELEVENLABS_UNSUPPORTED_LANGUAGES = {"mni", "brx"}


class PersonalizedVoiceService:
    """
    Service responsible for managing personalized voice cloning and
    generation via ElevenLabs.
    """

    def __init__(
        self,
        voice_profile: VoiceProfile,
        dataset: Optional[VoiceDatasetManager] = None,
        api_key: Optional[str] = None,
    ) -> None:
        if not voice_profile:
            raise ValueError("voice_profile is required.")

        self.voice_profile = voice_profile
        self.dataset = dataset

        self.api_key = api_key or os.getenv("ELEVENLABS_API_KEY")
        self.client = ElevenLabs(api_key=self.api_key) if self.api_key else None

        logger.info("Personalized voice service initialized: %s", voice_profile.voice_id)

    def is_configured(self) -> bool:
        """Whether an ElevenLabs API key is available."""
        return bool(self.api_key)

    # ---------------------------------------------------------
    # Voice information
    # ---------------------------------------------------------

    def get_voice_id(self) -> str:
        """Return our own internal ID for the selected voice."""
        return self.voice_profile.voice_id

    def get_voice_name(self) -> str:
        return self.voice_profile.name

    def get_voice_language(self) -> str:
        return self.voice_profile.language

    def is_personalized(self) -> bool:
        return self.voice_profile.is_personalized

    def is_cloned(self) -> bool:
        """Whether this voice has actually been cloned via ElevenLabs yet."""
        return bool(self.voice_profile.external_voice_id)

    # ---------------------------------------------------------
    # Dataset information
    # ---------------------------------------------------------

    def get_dataset_duration(self) -> float:
        if self.dataset is None:
            return 0.0
        return self.dataset.get_total_duration()

    def get_recording_count(self) -> int:
        if self.dataset is None:
            return 0
        return self.dataset.get_recording_count()

    # ---------------------------------------------------------
    # Language support check
    # ---------------------------------------------------------

    def supports_language(self, language: str) -> bool:
        """
        Check whether this voice is configured for the given language,
        AND that ElevenLabs itself actually supports that language at all.

        Note: ElevenLabs' multilingual model can technically speak many
        languages regardless of what language the ORIGINAL clone
        recordings were in — but a voice cloned from English samples
        speaking Bengali would not actually sound authentic in that
        language, so the profile-language check is kept strict rather
        than relying on the model's cross-lingual capability.

        Separately: Manipuri and Bodo are NOT supported by ElevenLabs
        at all (confirmed via their docs — neither eleven_multilingual_v2
        nor eleven_v3 lists them), so this returns False for those
        codes regardless of the voice profile's own language field.
        Callers should fall back to the default AI voice (Gemini/
        Bhashini pipeline) for those two languages.
        """
        if language in ELEVENLABS_UNSUPPORTED_LANGUAGES:
            return False
        return self.voice_profile.language == language

    # ---------------------------------------------------------
    # Voice readiness
    # ---------------------------------------------------------

    def is_ready(
        self,
        language: Optional[str] = None,
        min_duration_seconds: Optional[float] = None,
    ) -> bool:
        """
        Check whether the personalized voice is ready to be used —
        meaning it has ALREADY been cloned (has an external_voice_id),
        not just that enough recordings exist to clone it.
        """
        if not self.voice_profile.is_available:
            return False
        if not self.voice_profile.is_personalized:
            return False
        if not self.is_cloned():
            return False
        if language is not None and not self.supports_language(language):
            return False
        return True

    def is_ready_to_clone(self, min_duration_seconds: Optional[float] = None) -> bool:
        """
        Check whether there's enough recorded audio to attempt cloning
        (distinct from is_ready(), which checks if cloning has ALREADY
        happened).
        """
        if self.dataset is None:
            return False
        if min_duration_seconds is not None:
            return self.dataset.is_ready_for_cloning(min_duration_seconds)
        return self.dataset.is_ready_for_cloning()

    # ---------------------------------------------------------
    # Clone the voice (one-time, via ElevenLabs Instant Voice Cloning)
    # ---------------------------------------------------------

    def clone_voice(self, description: str = "") -> str:
        """
        Create a real voice clone on ElevenLabs from this voice's
        recorded dataset. Only needs to be called ONCE per voice —
        after this succeeds, self.voice_profile.external_voice_id is
        set, and generate_speech() will use it for all future calls.

        Args:
            description: Optional description to help identify the
                voice later in the ElevenLabs dashboard.

        Returns:
            The ElevenLabs voice_id that was created.

        Raises:
            RuntimeError: If not configured, not enough recordings,
                or the ElevenLabs API call fails.
        """
        if not self.is_configured():
            raise RuntimeError(
                "ElevenLabs API key is not configured "
                "(set ELEVENLABS_API_KEY in .env)."
            )

        if not self.is_ready_to_clone():
            missing = (
                self.dataset.get_missing_duration_for_cloning()
                if self.dataset
                else "an unknown amount of"
            )
            raise RuntimeError(
                f"Not enough recorded audio to clone this voice yet "
                f"(~{missing}s more needed)."
            )

        file_paths: List[str] = [
            recording.file_path for recording in self.dataset.get_recordings()
        ]

        logger.info(
            "Cloning voice '%s' via ElevenLabs using %d recording(s)...",
            self.voice_profile.name,
            len(file_paths),
        )

        try:
            voice = self.client.voices.ivc.create(
                name=self.voice_profile.name,
                description=description or self.voice_profile.description,
                files=file_paths,
            )
        except Exception as exc:
            logger.exception("ElevenLabs voice cloning failed")
            raise RuntimeError(f"Voice cloning failed: {exc}") from exc

        self.voice_profile.external_voice_id = voice.voice_id
        logger.info("Voice cloned successfully. ElevenLabs voice_id=%s", voice.voice_id)

        return voice.voice_id

    # ---------------------------------------------------------
    # Generate speech using the cloned voice
    # ---------------------------------------------------------

    def generate_speech(
        self,
        text: str,
        language: Optional[str] = None,
        output_path: Optional[str] = None,
        model_id: str = DEFAULT_MODEL_ID,
    ) -> str:
        """
        Generate speech using the cloned personalized voice.

        Args:
            text: Text to speak.
            language: Optional language code to validate against this
                voice's configured language before generating anything.
            output_path: Path to save the generated audio. Defaults to
                a .mp3 file (ElevenLabs' native output format) if not
                given an explicit path — note this is NOT .wav, unlike
                Gemini/Bhashini TTS elsewhere in this project.
            model_id: ElevenLabs model to use. Defaults to
                eleven_multilingual_v2 (29 languages supported).

        Returns:
            Path to the generated audio file.

        Raises:
            ValueError: If text is empty, or the requested language
                doesn't match this voice's configured language.
            RuntimeError: If not configured, the voice hasn't been
                cloned yet, or the API call fails.
        """
        if not text or not text.strip():
            raise ValueError("text cannot be empty.")

        if language is not None and not self.supports_language(language):
            raise ValueError(
                f"Voice '{self.voice_profile.voice_id}' is configured for "
                f"language '{self.voice_profile.language}', not '{language}'. "
                "Use a different voice, or fall back to the default AI voice "
                "for this language."
            )

        if not self.is_configured():
            raise RuntimeError(
                "ElevenLabs API key is not configured "
                "(set ELEVENLABS_API_KEY in .env)."
            )

        if not self.is_ready(language=language):
            if not self.is_cloned():
                raise RuntimeError(
                    "This voice has not been cloned yet. Call clone_voice() first."
                )
            raise RuntimeError(
                "Personalized voice is not ready "
                "(unavailable, not personalized, or language mismatch)."
            )

        output_path = output_path or "personalized_response.mp3"

        logger.info(
            "Generating personalized speech using ElevenLabs voice_id=%s",
            self.voice_profile.external_voice_id,
        )

        try:
            audio = self.client.text_to_speech.convert(
                text=text.strip(),
                voice_id=self.voice_profile.external_voice_id,
                model_id=model_id,
                output_format=DEFAULT_OUTPUT_FORMAT,
            )
            audio_bytes = b"".join(chunk for chunk in audio)
        except Exception as exc:
            logger.exception("ElevenLabs speech generation failed")
            raise RuntimeError(f"Speech generation failed: {exc}") from exc

        with open(output_path, "wb") as audio_file:
            audio_file.write(audio_bytes)

        logger.info("Audio saved to %s", output_path)
        return output_path


# ---------------------------------------------------------
# Simple test
# ---------------------------------------------------------

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    from voice_profile import VoiceProfile
    from voice_dataset import VoiceDatasetManager, VoiceRecording

    voice = VoiceProfile(
        voice_id="family_voice_01",
        name="Family Voice",
        provider="elevenlabs",
        language="en",
        description="Personalized family member voice",
        is_personalized=True,
        is_available=True,
    )

    dataset = VoiceDatasetManager(voice_id="family_voice_01")
    # NOTE: replace with a REAL audio file path (a clean recording of
    # someone's voice, ideally 60+ seconds total across one or more
    # files) before running this for real.
    dataset.add_recording(
        VoiceRecording(
            recording_id="recording_001",
            file_path="tests/live_recording.wav",
            duration_seconds=90.0,
            language="en",
        )
    )

    service = PersonalizedVoiceService(voice_profile=voice, dataset=dataset)

    print("Configured:", service.is_configured())
    print("Ready to clone:", service.is_ready_to_clone())

    if service.is_configured() and service.is_ready_to_clone():
        print("\nCloning voice (this calls the real ElevenLabs API)...")
        try:
            voice_id = service.clone_voice(description="Test clone for SIH project")
            print(f"Cloned! ElevenLabs voice_id: {voice_id}")

            print("\nGenerating speech with the cloned voice...")
            output = service.generate_speech(
                text="Hello, this is a test of the cloned voice.",
                language="en",
                output_path="test_cloned_voice.mp3",
            )
            print(f"Audio saved to: {output}")
        except RuntimeError as exc:
            print(f"Error: {exc}")
    else:
        print("Skipping live test — set ELEVENLABS_API_KEY and add a real audio file first.")