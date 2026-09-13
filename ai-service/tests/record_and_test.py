import sounddevice as sd
from scipy.io.wavfile import write
from pathlib import Path

from voice_companion.speech_to_text import SpeechToText

DURATION = 60 # seconds
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
    result = stt.transcribe(audio_path=str(OUTPUT_PATH), language="en")

    print("\nTranscription:")
    print(result)