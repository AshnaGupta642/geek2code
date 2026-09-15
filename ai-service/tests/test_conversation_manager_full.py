"""
Full end-to-end test for ConversationManager.

Before running:
1. Place a real audio file in data/sample_memories/ (e.g. live_recording.wav)
2. In a separate terminal: cd data/sample_memories && python -m http.server 8000
3. Update AUDIO_URL below to match your actual filename
4. Run this from the project root: python tests/test_conversation_manager_full.py
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from voice_companion.conversation_manager import ConversationManager

AUDIO_URL = "http://localhost:8000/live_recording.wav"  # update to your actual file
LANGUAGE = "en"  # try "en"/"hi"/"bn" first, then a regional code like "ml"/"brx"/"as"/"mni"
CONVERSATION_ID = "test_convo_001"  # reuse this same ID to test multi-turn memory


def print_result(result: dict) -> None:
    print("\n" + "=" * 60)
    print("RESULT")
    print("=" * 60)
    for key, value in result.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    manager = ConversationManager()

    try:
        result = manager.process_conversation(
            patient_id="P001",
            audio_url=AUDIO_URL,
            language=LANGUAGE,
            conversation_id=CONVERSATION_ID,
        )
        print_result(result)

        print(f"\nOpen this file to listen to the response: {result['response_audio_url']}")

    except (ValueError, RuntimeError) as err:
        print(f"Error: {err}")