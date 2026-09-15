import logging
import os
import wave
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import APIError

load_dotenv()

logger = logging.getLogger(__name__)

DEFAULT_MODEL = "gemini-3.1-flash-tts-preview"
DEFAULT_VOICE = "Kore"

# Gemini's native TTS output format (per API docs)
PCM_SAMPLE_RATE = 24000
PCM_SAMPLE_WIDTH_BYTES = 2  # 16-bit
PCM_CHANNELS = 1  # mono

OUTPUT_DIR = Path(__file__).parent.parent / "data" / "audio_responses"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


class TextToSpeech:
    """Convert AI-generated text into speech using the Gemini API."""

    def __init__(
        self,
        model: str = DEFAULT_MODEL,
        voice: str = DEFAULT_VOICE,
        api_key: Optional[str] = None,
    ):
        api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set. Check your .env file.")

        self.model = model
        self.voice = voice
        self.client = genai.Client(api_key=api_key)

    def synthesize(
        self,
        text: str,
        output_path: Optional[str] = None,
    ) -> str:
        """
        Convert text into speech and save it as a playable WAV file.

        Args:
            text: Text that should be spoken.
            output_path: Optional path for the generated audio file.

        Returns:
            Path to the generated audio file.

        Raises:
            ValueError: If text is empty.
            RuntimeError: If the Gemini API call fails or returns no audio.
        """
        if not text or not text.strip():
            raise ValueError("text cannot be empty.")

        if output_path is None:
            output_path = str(OUTPUT_DIR / "response.wav")

        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        logger.info("Generating speech using model=%s, voice=%s", self.model, self.voice)

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=text.strip(),
                config=types.GenerateContentConfig(
                    response_modalities=["AUDIO"],
                    speech_config=types.SpeechConfig(
                        voice_config=types.VoiceConfig(
                            prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                voice_name=self.voice
                            )
                        )
                    ),
                ),
            )
        except APIError as exc:
            logger.exception("Text-to-speech request failed")
            raise RuntimeError(f"Text-to-speech request failed: {exc}") from exc

        try:
            pcm_data = response.candidates[0].content.parts[0].inline_data.data
            if not pcm_data:
                raise ValueError("Empty audio payload")
        except (AttributeError, IndexError, TypeError, ValueError) as exc:
            logger.exception("No audio data returned by Gemini")
            raise RuntimeError("Gemini returned no usable audio data.") from exc

        # Gemini returns raw PCM — wrap it in a proper WAV header before saving.
        with wave.open(str(output_file), "wb") as wav_file:
            wav_file.setnchannels(PCM_CHANNELS)
            wav_file.setsampwidth(PCM_SAMPLE_WIDTH_BYTES)
            wav_file.setframerate(PCM_SAMPLE_RATE)
            wav_file.writeframes(pcm_data)

        logger.info("Audio saved to %s", output_file)
        return str(output_file)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    tts = TextToSpeech()

    try:
        text = input("AI response: ")
        output = tts.synthesize(
            text=text,
            output_path=str(OUTPUT_DIR / "test_response.wav"),
        )
        print("\nAudio generated successfully:")
        print(output)
    except (ValueError, RuntimeError) as err:
        print(f"Error: {err}")