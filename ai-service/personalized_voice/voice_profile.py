"""
Voice Profile

Stores information about available voices and the currently
selected/preferred voice.

This file does NOT create or clone a voice.
It only manages voice profiles so that a real personalized
voice can be added later.
"""

import logging
from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class VoiceProfile:
    """Information about one voice."""

    voice_id: str
    name: str
    provider: str = "local"
    language: str = "en"
    description: str = ""
    is_personalized: bool = False
    is_available: bool = True
    # The voice ID assigned by the actual cloning provider (e.g.
    # ElevenLabs), once cloning has succeeded. This is DIFFERENT from
    # `voice_id` above, which is OUR OWN internal identifier used for
    # dataset keys and selection — external_voice_id is what actually
    # gets passed to the provider's text-to-speech call. None until
    # a real clone has been created via VoiceService.clone_voice().
    external_voice_id: Optional[str] = None


class VoiceProfileManager:
    """Manages available voices and the currently selected voice."""

    def __init__(self) -> None:
        self.voices: Dict[str, VoiceProfile] = {}
        self.selected_voice_id: Optional[str] = None

    def add_voice(self, voice: VoiceProfile) -> None:
        if not voice.voice_id:
            raise ValueError("voice_id cannot be empty.")
        if voice.voice_id in self.voices:
            logger.warning("Overwriting existing voice profile: %s", voice.voice_id)
        self.voices[voice.voice_id] = voice
        logger.info("Added voice: %s (%s)", voice.voice_id, voice.name)

    def remove_voice(self, voice_id: str) -> bool:
        if voice_id not in self.voices:
            return False
        del self.voices[voice_id]
        if self.selected_voice_id == voice_id:
            self.selected_voice_id = None
        logger.info("Removed voice: %s", voice_id)
        return True

    def select_voice(self, voice_id: str) -> None:
        if voice_id not in self.voices:
            raise ValueError(f"Voice '{voice_id}' does not exist.")
        voice = self.voices[voice_id]
        if not voice.is_available:
            raise ValueError(f"Voice '{voice_id}' is currently unavailable.")
        self.selected_voice_id = voice_id
        logger.info("Selected voice: %s", voice_id)

    def set_availability(self, voice_id: str, is_available: bool) -> None:
        if voice_id not in self.voices:
            raise ValueError(f"Voice '{voice_id}' does not exist.")
        self.voices[voice_id].is_available = is_available
        if not is_available and self.selected_voice_id == voice_id:
            self.selected_voice_id = None

    def get_selected_voice(self) -> Optional[VoiceProfile]:
        if self.selected_voice_id is None:
            return None
        return self.voices.get(self.selected_voice_id)

    def get_available_voices(self, language: Optional[str] = None) -> List[VoiceProfile]:
        voices = [voice for voice in self.voices.values() if voice.is_available]
        if language:
            voices = [voice for voice in voices if voice.language == language]
        return voices

    def get_selected_voice_data(self) -> Optional[Dict[str, Any]]:
        voice = self.get_selected_voice()
        if voice is None:
            return None
        return asdict(voice)