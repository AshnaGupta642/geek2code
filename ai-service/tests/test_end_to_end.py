import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent / "voice_companion"))

import sounddevice as sd
from scipy.io.wavfile import write

from voice_companion.speech_to_text import SpeechToText
from voice_companion.llm_client import LLMClient

DURATION = 8
SAMPLE_RATE = 44100
OUTPUT_PATH = Path(__file__).parent / "live_recording.wav"


def record_audio(duration: int, fs: int, output_path: Path) -> None:
    print(f"Recording for {duration} seconds... speak now.")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    write(str(output_path), fs, recording)
    print(f"Saved recording to {output_path}")


if __name__ == "__main__":
    record_audio(DURATION, SAMPLE_RATE, OUTPUT_PATH)

    stt = SpeechToText()
    llm = LLMClient()

    try:
        transcript = stt.transcribe(audio_path=str(OUTPUT_PATH), language="en")
        print(f"\nPatient said: {transcript}")

        response = llm.generate_response(transcript)
        print(f"\nAI Companion: {response}")

    except (FileNotFoundError, ValueError, RuntimeError) as err:
        print(f"Error: {err}")