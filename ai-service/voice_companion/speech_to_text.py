import logging
import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import APIError

load_dotenv()

logger = logging.getLogger(__name__)

SUPPORTED_FORMATS = {".wav", ".mp3", ".m4a", ".mp4", ".mpeg", ".mpga", ".webm"}
DEFAULT_MODEL = "gemini-3.5-transcribe"

MIME_TYPES = {
    ".wav": "audio/wav",
    ".mp3": "audio/mp3",
    ".m4a": "audio/mp4",
    ".mp4": "audio/mp4",
    ".mpeg": "audio/mpeg",
    ".mpga": "audio/mpeg",
    ".webm": "audio/webm",
}


class SpeechToText:
    """Convert patient's voice/audio into text using the Gemini API."""

    def __init__(self, model: str = DEFAULT_MODEL, api_key: Optional[str] = None):
        api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set (check your .env file).")

        self.model = model
        self.client = genai.Client(api_key=api_key)

    @staticmethod
    def _validate_audio(path: Path) -> None:
        if not path.exists():
            raise FileNotFoundError(f"Audio file not found: {path}")
        if not path.is_file():
            raise ValueError(f"Path is not a file: {path}")
        if path.suffix.lower() not in SUPPORTED_FORMATS:
            raise ValueError(
                f"Unsupported audio format '{path.suffix}'. "
                f"Supported: {', '.join(sorted(SUPPORTED_FORMATS))}"
            )
        if path.stat().st_size == 0:
            raise ValueError(f"Audio file is empty: {path}")

    def transcribe(
        self,
        audio_path: str,
        language: Optional[str] = None,
        prompt: Optional[str] = None,
    ) -> str:
        """
        Convert an audio file into text.

        Args:
            audio_path: Path to the audio file.
            language: Optional language name/code hint, e.g. "en" or "hi".
                gemini-3.5-transcribe auto-detects language, but this can help.
            prompt: Optional context/vocabulary hint (e.g. medical terms, names).

        Returns:
            Transcribed text.

        Raises:
            FileNotFoundError: If the audio file doesn't exist.
            ValueError: If the file is invalid or unsupported.
            RuntimeError: If the API call fails.
        """
        path = Path(audio_path)
        self._validate_audio(path)

        mime_type = MIME_TYPES.get(path.suffix.lower(), "audio/mpeg")

        logger.info("Transcribing %s (model=%s, language=%s)", path, self.model, language)

        try:
            uploaded_file = self.client.files.upload(
                file=str(path),
                config=types.UploadFileConfig(mime_type=mime_type),
            )

            input_parts = [
                {
                    "type": "audio",
                    "uri": uploaded_file.uri,
                    "mime_type": uploaded_file.mime_type,
                }
            ]

            interaction = self.client.interactions.create(
                model=self.model,
                input=input_parts,
            )
        except APIError as exc:
            logger.exception("Transcription failed for %s", path)
            raise RuntimeError(f"Transcription failed: {exc}") from exc

        text = (interaction.output_text or "").strip()
        if not text:
            logger.warning("Transcription returned empty text for %s", path)

        return text


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    stt = SpeechToText()

    try:
        result = stt.transcribe(audio_path="sample_audio.wav", language="en")
        print("Transcription:")
        print(result)
    except (FileNotFoundError, ValueError, RuntimeError) as err:
        print(f"Error: {err}")