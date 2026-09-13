import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent / "voice_companion"))

import sounddevice as sd
import winsound
from scipy.io.wavfile import write

from voice_companion.speech_to_text import SpeechToText
from voice_companion.llm_client import LLMClient
from voice_companion.text_to_speech import TextToSpeech

DURATION = 8
SAMPLE_RATE = 44100
RECORDING_PATH = Path(__file__).parent / "live_recording.wav"


def record_audio(duration: int, fs: int, output_path: Path) -> None:
    print(f"Recording for {duration} seconds... speak now.")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    write(str(output_path), fs, recording)
    print(f"Saved recording to {output_path}")


def play_audio(path: str) -> None:
    winsound.PlaySound(path, winsound.SND_FILENAME)


if __name__ == "__main__":
    record_audio(DURATION, SAMPLE_RATE, RECORDING_PATH)

    stt = SpeechToText()
    llm = LLMClient()
    tts = TextToSpeech()

    try:
        transcript = stt.transcribe(audio_path=str(RECORDING_PATH), language="en")
        print(f"\nPatient said: {transcript}")

        response = llm.generate_response(transcript)
        print(f"\nAI Companion: {response}")

        audio_path = tts.synthesize(text=response)
        print(f"\nSpeaking response...")
        play_audio(audio_path)

    except (FileNotFoundError, ValueError, RuntimeError) as err:
        print(f"Error: {err}")