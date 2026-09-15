"""
Voice Dataset Manager

Manages voice recordings that can later be used for
personalized voice generation.

This file:
- stores recording information
- adds recordings
- removes recordings
- lists recordings
- calculates total recording duration
- checks whether the dataset has enough audio for cloning

It does NOT create or clone a voice.
"""

import logging
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

# Most real voice-cloning providers need a minimum amount of clean
# audio before cloning produces usable results. This is a rough,
# conservative default — adjust once you pick an actual provider.
MIN_DURATION_FOR_CLONING_SECONDS = 60.0
MIN_USEFUL_RECORDING_SECONDS = 1.0


# ---------------------------------------------------------
# Voice Recording
# ---------------------------------------------------------

@dataclass
class VoiceRecording:
    """
    Information about one voice recording.
    """

    recording_id: str
    file_path: str
    duration_seconds: float
    language: str = "en"
    transcript: str = ""


# ---------------------------------------------------------
# Voice Dataset Manager
# ---------------------------------------------------------

class VoiceDatasetManager:
    """
    Manages recordings belonging to a personalized voice.
    """

    def __init__(self, voice_id: str) -> None:
        if not voice_id:
            raise ValueError("voice_id cannot be empty.")

        self.voice_id = voice_id
        self.recordings: Dict[str, VoiceRecording] = {}

    # -----------------------------------------------------
    # Add recording
    # -----------------------------------------------------

    def add_recording(self, recording: VoiceRecording) -> None:
        """
        Add a voice recording to the dataset.
        Overwrites any existing recording with the same recording_id.
        """
        if not recording.recording_id:
            raise ValueError("recording_id cannot be empty.")

        if not recording.file_path:
            raise ValueError("file_path cannot be empty.")

        if recording.duration_seconds < 0:
            raise ValueError("duration_seconds cannot be negative.")

        if recording.recording_id in self.recordings:
            logger.warning(
                "Overwriting existing recording: %s", recording.recording_id
            )

        if recording.duration_seconds < MIN_USEFUL_RECORDING_SECONDS:
            logger.warning(
                "Recording '%s' is very short (%.2fs) and may not be useful for voice training.",
                recording.recording_id,
                recording.duration_seconds,
            )

        self.recordings[recording.recording_id] = recording
        logger.info(
            "Added recording: %s (%.2fs)", recording.recording_id, recording.duration_seconds
        )

    # -----------------------------------------------------
    # Remove recording
    # -----------------------------------------------------

    def remove_recording(self, recording_id: str) -> bool:
        """
        Remove a recording from the dataset.

        Returns:
            True if removed, False if not found.
        """
        if recording_id not in self.recordings:
            return False

        del self.recordings[recording_id]
        logger.info("Removed recording: %s", recording_id)
        return True

    # -----------------------------------------------------
    # Get recording
    # -----------------------------------------------------

    def get_recording(self, recording_id: str) -> Optional[VoiceRecording]:
        """
        Get one recording by ID.
        """
        return self.recordings.get(recording_id)

    # -----------------------------------------------------
    # Get all recordings (optionally filtered by language)
    # -----------------------------------------------------

    def get_recordings(self, language: Optional[str] = None) -> List[VoiceRecording]:
        """
        Return all recordings, optionally filtered by language.
        """
        recordings = list(self.recordings.values())

        if language:
            recordings = [r for r in recordings if r.language == language]

        return recordings

    # -----------------------------------------------------
    # Total duration
    # -----------------------------------------------------

    def get_total_duration(self) -> float:
        """
        Calculate total recording duration in seconds.
        """
        return sum(recording.duration_seconds for recording in self.recordings.values())

    # -----------------------------------------------------
    # Number of recordings
    # -----------------------------------------------------

    def get_recording_count(self) -> int:
        """
        Return the number of recordings.
        """
        return len(self.recordings)

    # -----------------------------------------------------
    # Check files
    # -----------------------------------------------------

    def check_files(self) -> Dict[str, bool]:
        """
        Check whether the recording files actually exist on disk.

        Returns:
            Dictionary mapping recording IDs to True/False.
        """
        return {
            recording_id: Path(recording.file_path).exists()
            for recording_id, recording in self.recordings.items()
        }

    # -----------------------------------------------------
    # Cloning readiness check
    # -----------------------------------------------------

    def is_ready_for_cloning(
        self, min_duration_seconds: float = MIN_DURATION_FOR_CLONING_SECONDS
    ) -> bool:
        """
        Check whether this dataset has enough total audio duration
        to be usable for voice cloning. This does NOT check audio
        quality — only quantity.
        """
        return self.get_total_duration() >= min_duration_seconds

    def get_missing_duration_for_cloning(
        self, min_duration_seconds: float = MIN_DURATION_FOR_CLONING_SECONDS
    ) -> float:
        """
        Return how many more seconds of audio are needed to reach
        the cloning readiness threshold. Returns 0.0 if already ready.
        """
        remaining = min_duration_seconds - self.get_total_duration()
        return max(0.0, remaining)

    # -----------------------------------------------------
    # Export dataset information
    # -----------------------------------------------------

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the complete dataset into a dictionary.

        Useful when sending dataset information to the backend.
        """
        return {
            "voice_id": self.voice_id,
            "recordings": [asdict(recording) for recording in self.recordings.values()],
            "recording_count": self.get_recording_count(),
            "total_duration_seconds": self.get_total_duration(),
            "is_ready_for_cloning": self.is_ready_for_cloning(),
        }


# ---------------------------------------------------------
# Simple Test
# ---------------------------------------------------------

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    dataset = VoiceDatasetManager(voice_id="family_voice_01")

    recording_1 = VoiceRecording(
        recording_id="recording_001",
        file_path="recordings/sample_001.wav",
        duration_seconds=12.5,
        language="en",
        transcript="Hello, how are you today?",
    )

    recording_2 = VoiceRecording(
        recording_id="recording_002",
        file_path="recordings/sample_002.wav",
        duration_seconds=15.2,
        language="en",
        transcript="I am happy to talk with you.",
    )

    dataset.add_recording(recording_1)
    dataset.add_recording(recording_2)

    print("\nRECORDINGS:")
    for recording in dataset.get_recordings():
        print(f"- {recording.recording_id}: {recording.duration_seconds}s")

    print("\nDATASET INFORMATION:")
    print("Voice ID:", dataset.voice_id)
    print("Number of recordings:", dataset.get_recording_count())
    print("Total duration:", dataset.get_total_duration(), "seconds")
    print("Ready for cloning:", dataset.is_ready_for_cloning())
    print("Still needed for cloning:", dataset.get_missing_duration_for_cloning(), "seconds")

    print("\nDATASET DICTIONARY:")
    print(dataset.to_dict())