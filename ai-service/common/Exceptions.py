"""
Common Exceptions

A small custom exception hierarchy for the AI engine.

IMPORTANT — backward compatibility:
Every file built so far raises plain ValueError/RuntimeError, and
every file's error handling catches those same plain types (e.g.
`except (ValueError, RuntimeError) as err:` appears throughout
voice_companion/, language_engine/, memory_vault/). To avoid breaking
any of that, every exception here EXTENDS ValueError or RuntimeError
rather than replacing them — so `except RuntimeError` still catches
a TranscriptionError, and existing code needs zero changes.

These are OPTIONAL for new code to use going forward — adopting them
lets calling code catch a specific failure type (e.g. "was it
transcription that failed, or translation?") without needing to
parse error message strings, but nothing existing is required to
switch to them.
"""


class AIEngineError(Exception):
    """
    Base class for all custom exceptions in this project. Not used
    directly — exists only so `except AIEngineError` can catch any
    of the specific errors below in one place if ever needed.
    Does NOT extend ValueError/RuntimeError itself; the concrete
    subclasses below do that individually, matching whichever of the
    two each replaces in existing code.
    """


class UnsupportedLanguageError(ValueError, AIEngineError):
    """
    Raised for a language code that isn't one of the 7 supported by
    language_engine/language_config.py. Extends ValueError since
    that's what is_supported() checks already raised everywhere
    (e.g. conversation_manager.py, translator.py).
    """


class TranscriptionError(RuntimeError, AIEngineError):
    """
    Raised when speech-to-text fails (Gemini or Bhashini), after
    retries/fallbacks have been exhausted. Extends RuntimeError to
    match speech_to_text.py's and speech_language_router.py's
    existing raise type.
    """


class TranslationError(RuntimeError, AIEngineError):
    """
    Raised when translation fails (Gemini or Bhashini), after
    retries/fallbacks have been exhausted. Extends RuntimeError to
    match translator.py's existing raise type.
    """


class SpeechSynthesisError(RuntimeError, AIEngineError):
    """
    Raised when text-to-speech fails (Gemini or Bhashini), after
    retries/fallbacks have been exhausted. Extends RuntimeError to
    match text_to_speech.py's existing raise type.
    """


class MemoryExtractionError(RuntimeError, AIEngineError):
    """
    Raised when memory/entity extraction fails (memory_extractor.py,
    entity_extractor.py) after retries. Extends RuntimeError to match
    those files' existing raise type.
    """


class VoiceNotReadyError(RuntimeError, AIEngineError):
    """
    Raised when a personalized voice is requested but isn't ready
    (insufficient recordings, wrong language, unavailable). Extends
    RuntimeError to match voice_service.py's existing raise type.
    """


class ConversationStateError(RuntimeError, AIEngineError):
    """
    Raised for conversation/context-management failures not covered
    by the more specific errors above (e.g. an invalid conversation_id
    state). Extends RuntimeError.
    """


# ---------------------------------------------------------
# Simple test
# ---------------------------------------------------------

if __name__ == "__main__":
    # Confirm each custom exception is still catchable by the plain
    # built-in type existing code already catches everywhere.
    try:
        raise UnsupportedLanguageError("French is not supported.")
    except ValueError as exc:
        print(f"Caught as ValueError: {exc}")

    try:
        raise TranscriptionError("Bhashini ASR failed after 3 attempts.")
    except RuntimeError as exc:
        print(f"Caught as RuntimeError: {exc}")

    try:
        raise TranslationError("Translation failed.")
    except AIEngineError as exc:
        print(f"Caught as AIEngineError (specific-type catch): {exc}")

    # Confirm the base class does NOT accidentally catch built-in
    # ValueError/RuntimeError raised the old way (it shouldn't, and mustn't).
    try:
        raise ValueError("A plain old ValueError, unrelated to this module.")
    except AIEngineError:
        print("BUG: this should not have been caught as AIEngineError!")
    except ValueError as exc:
        print(f"Correctly NOT caught as AIEngineError; caught as ValueError: {exc}")