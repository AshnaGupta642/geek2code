"""
Common Config

Centralized shared settings for the AI engine.

IMPORTANT — this does NOT replace per-file constants that already
exist and work (e.g. DEFAULT_MODEL in llm_client.py, memory_extractor.py,
etc., or AUDIO_OUTPUT_DIR duplicated in text_to_speech.py and
conversation_manager.py). Rewriting every existing file to import from
here instead would be a large, risky refactor for something that's
already working correctly. Instead, this file exists so:
    1. NEW code has one obvious place to put shared settings, instead
       of each new file reinventing its own constant.
    2. A few genuinely cross-cutting values (like the project root
       path, or shared timeout defaults) have one source of truth
       going forward, even though older files keep their own local
       copies for now.

If you want to consolidate the older per-file constants into this
file later, that's a reasonable follow-up — just not done here, to
avoid touching many already-working, tested files at once.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------
# Project paths
# ---------------------------------------------------------
# Assumes this file lives at <project_root>/common/config.py.
PROJECT_ROOT = Path(__file__).parent.parent

DATA_DIR = PROJECT_ROOT / "data"
AUDIO_RESPONSES_DIR = DATA_DIR / "audio_responses"
SAMPLE_MEMORIES_DIR = DATA_DIR / "sample_memories"
LANGUAGE_TEST_DATA_DIR = DATA_DIR / "language_test_data"

for _dir in (AUDIO_RESPONSES_DIR, SAMPLE_MEMORIES_DIR, LANGUAGE_TEST_DATA_DIR):
    _dir.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------
# API credentials (read once here; individual files can still read
# os.getenv() directly too — both approaches coexist safely)
# ---------------------------------------------------------
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
BHASHINI_USER_ID = os.getenv("BHASHINI_USER_ID")
BHASHINI_API_KEY = os.getenv("BHASHINI_API_KEY")


def require_gemini_api_key() -> str:
    """Return GEMINI_API_KEY, raising a clear error if it's missing."""
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is not set. Add it to your .env file.")
    return GEMINI_API_KEY


def bhashini_is_configured() -> bool:
    """Whether both Bhashini credentials are present."""
    return bool(BHASHINI_USER_ID and BHASHINI_API_KEY)


# ---------------------------------------------------------
# Shared defaults
# ---------------------------------------------------------
DEFAULT_REQUEST_TIMEOUT_SECONDS = 20
DEFAULT_MAX_RETRIES = 3
DEFAULT_RETRY_BASE_DELAY_SECONDS = 2  # doubles each retry: 2s, 4s, 8s

# Matches ContextManager's own default, kept here too so new code
# doesn't need to import context_manager.py just to know this number.
DEFAULT_MAX_CONVERSATION_MESSAGES = 10

# Matches VoiceDatasetManager's own default cloning threshold.
DEFAULT_MIN_CLONING_DURATION_SECONDS = 60.0


# ---------------------------------------------------------
# Simple test
# ---------------------------------------------------------

if __name__ == "__main__":
    print("PROJECT_ROOT:", PROJECT_ROOT)
    print("AUDIO_RESPONSES_DIR:", AUDIO_RESPONSES_DIR)
    print("SAMPLE_MEMORIES_DIR:", SAMPLE_MEMORIES_DIR)
    print("LANGUAGE_TEST_DATA_DIR:", LANGUAGE_TEST_DATA_DIR)
    print()
    print("GEMINI_API_KEY present:", bool(GEMINI_API_KEY))
    print("Bhashini configured:", bhashini_is_configured())