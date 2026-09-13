import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent / "voice_companion"))

import winsound
from text_to_speech import TextToSpeech


def play_audio(path: str) -> None:
    winsound.PlaySound(path, winsound.SND_FILENAME)


def main():
    tts = TextToSpeech()

    print("Text-to-Speech test — type 'quit' to exit.\n")

    while True:
        text = input("Text to speak: ").strip()

        if text.lower() in {"quit", "exit"}:
            print("Ending session.")
            break

        if not text:
            continue

        try:
            output_path = tts.synthesize(text=text)
            print(f"Saved to: {output_path}")
            print("Playing audio...")
            play_audio(output_path)
            print()
        except (ValueError, RuntimeError) as err:
            print(f"Error: {err}\n")


if __name__ == "__main__":
    main()