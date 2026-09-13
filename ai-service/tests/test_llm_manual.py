import sys
from pathlib import Path

# Allow importing from voice_companion/ regardless of where this is run from
sys.path.append(str(Path(__file__).parent.parent / "voice_companion"))

from voice_companion.llm_client import LLMClient


def main():
    llm = LLMClient()

    print("AI Companion test — type 'quit' to exit.\n")

    while True:
        user_text = input("Patient: ").strip()

        if user_text.lower() in {"quit", "exit"}:
            print("Ending session.")
            break

        if not user_text:
            continue

        try:
            result = llm.generate_response(user_text)
            print(f"AI Companion: {result}\n")
        except (ValueError, RuntimeError) as err:
            print(f"Error: {err}\n")


if __name__ == "__main__":
    main()