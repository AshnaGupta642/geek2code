"""
Language Configuration

Central source of truth for every language the AI Voice Companion
supports. Other files in language_engine/ (and voice_companion/'s
prompts.py, conversation_manager.py) should import from here rather
than hardcoding language codes/names separately, so updating the
supported language list — or which provider handles which language —
only ever requires editing this one file.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional

# ---------------------------------------------------------
# Providers
# ---------------------------------------------------------
# Each language is handled by exactly one provider for STT/LLM/TTS.
# "GEMINI" languages use the existing Gemini-based speech_to_text.py /
# llm_client.py / text_to_speech.py directly.
# "REGIONAL_API" languages route through a separate Indian-language
# API instead — specifically Bhashini (Govt of India's National
# Language Translation Mission API), chosen for its strong coverage
# of Northeast Indian languages like Manipuri and Bodo that most
# mainstream providers don't support well.

PROVIDER_GEMINI = "GEMINI"
PROVIDER_REGIONAL_API = "REGIONAL_API"

REGIONAL_API_PROVIDER_NAME = "Bhashini"

# Bhashini identifies languages by ISO 639 codes similar to what's
# used here, but confirm the exact codes/service IDs it expects for
# each language against Bhashini's own API docs before wiring up
# speech_language_router.py — some services key language pairs by
# a "serviceId" rather than a plain language code.


# ---------------------------------------------------------
# Supported languages
# ---------------------------------------------------------
# Codes follow ISO 639-1 where one exists (en, hi, bn, ml, as).
# Manipuri (Meitei) and Bodo have no widely-used ISO 639-1 code, so
# ISO 639-3 codes are used instead (mni, brx) for consistency.


@dataclass(frozen=True)
class LanguageInfo:
    """Static information about one supported language."""

    code: str
    english_name: str
    native_name: str
    # Instruction handed to the LLM to make it respond in this language.
    # Only meaningful for provider == PROVIDER_GEMINI; regional-API
    # languages generate responses through that API's own mechanism
    # instead, so this is left as a plain fallback string for them.
    response_instruction: str
    # Which provider handles STT/LLM/TTS for this language.
    provider: str


SUPPORTED_LANGUAGES: Dict[str, LanguageInfo] = {
    "en": LanguageInfo(
        code="en",
        english_name="English",
        native_name="English",
        response_instruction="Respond in English.",
        provider=PROVIDER_GEMINI,
    ),
    "hi": LanguageInfo(
        code="hi",
        english_name="Hindi",
        native_name="हिन्दी",
        response_instruction="Respond in Hindi.",
        provider=PROVIDER_GEMINI,
    ),
    "bn": LanguageInfo(
        code="bn",
        english_name="Bengali",
        native_name="বাংলা",
        response_instruction="Respond in Bengali.",
        provider=PROVIDER_GEMINI,
    ),
    "as": LanguageInfo(
        code="as",
        english_name="Assamese",
        native_name="অসমীয়া",
        response_instruction="Respond in Assamese.",
        provider=PROVIDER_REGIONAL_API,
    ),
    "ml": LanguageInfo(
        code="ml",
        english_name="Malayalam",
        native_name="മലയാളം",
        response_instruction="Respond in Malayalam.",
        provider=PROVIDER_REGIONAL_API,
    ),
    "mni": LanguageInfo(
        code="mni",
        english_name="Manipuri",
        native_name="মৈতৈলোন্ (Meitei)",
        response_instruction="Respond in Manipuri (Meitei).",
        provider=PROVIDER_REGIONAL_API,
    ),
    "brx": LanguageInfo(
        code="brx",
        english_name="Bodo",
        native_name="बर'",
        response_instruction="Respond in Bodo.",
        provider=PROVIDER_REGIONAL_API,
    ),
}

DEFAULT_LANGUAGE_CODE = "en"


# ---------------------------------------------------------
# Lookup helpers
# ---------------------------------------------------------


def is_supported(language_code: str) -> bool:
    """Check whether a language code is supported."""
    return language_code in SUPPORTED_LANGUAGES


def get_language_info(language_code: str) -> Optional[LanguageInfo]:
    """
    Return the LanguageInfo for a code, or None if unsupported.
    Callers that need a hard failure on an unknown code should check
    is_supported() first and raise their own ValueError with context
    (e.g. conversation_manager.py already does this).
    """
    return SUPPORTED_LANGUAGES.get(language_code)


def get_response_instruction(language_code: str) -> str:
    """
    Return the LLM instruction for a language code.
    Falls back to a generic instruction naming the raw code if it's
    not in SUPPORTED_LANGUAGES, rather than raising — this mirrors
    the previous behavior in prompts.py's get_language_instruction(),
    so an unexpected code degrades gracefully instead of crashing
    a live conversation.
    """
    info = get_language_info(language_code)
    if info:
        return info.response_instruction
    return f"Respond in the requested language: {language_code}."


def get_provider(language_code: str) -> str:
    """
    Return which provider (PROVIDER_GEMINI or PROVIDER_REGIONAL_API)
    handles this language. Defaults to PROVIDER_GEMINI for an unknown
    code, matching Gemini's role as the general-purpose fallback.
    """
    info = get_language_info(language_code)
    return info.provider if info else PROVIDER_GEMINI


def uses_gemini(language_code: str) -> bool:
    """Convenience check: does this language route through Gemini?"""
    return get_provider(language_code) == PROVIDER_GEMINI


def uses_regional_api(language_code: str) -> bool:
    """Convenience check: does this language route through the regional API?"""
    return get_provider(language_code) == PROVIDER_REGIONAL_API


def get_all_language_codes() -> List[str]:
    """Return all supported language codes."""
    return list(SUPPORTED_LANGUAGES.keys())


def get_all_languages() -> List[LanguageInfo]:
    """Return LanguageInfo for every supported language."""
    return list(SUPPORTED_LANGUAGES.values())


def get_languages_by_provider(provider: str) -> List[LanguageInfo]:
    """Return all languages handled by a given provider."""
    return [lang for lang in SUPPORTED_LANGUAGES.values() if lang.provider == provider]


def get_language_name(language_code: str) -> str:
    """
    Return the English display name for a language code.
    Falls back to the raw code if unsupported.
    """
    info = get_language_info(language_code)
    return info.english_name if info else language_code


# ---------------------------------------------------------
# Previously-supported languages (dropped from the current list)
# ---------------------------------------------------------
# Earlier project drafts supported Khasi and Mizo. They were dropped
# from the current 7-language list, but a patient/app could still
# send one of these codes (old app version, stale config, etc.).
# These get a slightly different message than a totally unknown code,
# acknowledging them by name rather than treating them as a typo.

PREVIOUSLY_SUPPORTED_LANGUAGES: Dict[str, str] = {
    "kh": "Khasi",
    "lus": "Mizo",
}

# Visual-only marker for unsupported-language messages. Language-independent,
# so it reads as "something's wrong" regardless of what language the
# person on screen reads — useful for app/screen display. Never pass
# include_emoji=True when the message is going into text_to_speech.py,
# since an emoji has no clean spoken form and would sound odd or be
# silently dropped by TTS.
UNSUPPORTED_LANGUAGE_EMOJI = "⚠️🌐"

# The spoken (TTS) rejection message is kept in English and Hindi only —
# not translated into all 7 supported languages. Two reasons:
# 1. Translating into all 7 (especially Bodo/Manipuri, where Gemini's own
#    translation quality is uncertain) adds latency and unverified text
#    for a message patients should rarely ever hear in the first place.
# 2. English + Hindi covers the broadest share of users; everyone else
#    still gets the language-independent emoji version on screen (see
#    get_unsupported_language_message(..., include_emoji=True)), which
#    doesn't require reading English or Hindi at all.
_UNSUPPORTED_TEMPLATES: Dict[str, str] = {
    "en": "{name} is not supported yet. Please try one of: {codes}.",
    "hi": "{name} अभी उपलब्ध नहीं है। कृपया इनमें से कोई आज़माएं: {codes}.",
}

_UNKNOWN_CODE_TEMPLATES: Dict[str, str] = {
    "en": "'{code}' is not a supported language right now. Please try one of: {names}.",
    "hi": "'{code}' अभी समर्थित भाषा नहीं है। कृपया इनमें से कोई आज़माएं: {names}.",
}


def get_unsupported_language_message(
    language_code: str,
    include_emoji: bool = False,
    message_language: str = "en",
) -> str:
    """
    Build a friendly, patient-facing message for a language code that
    isn't currently supported — used by conversation_manager.py (or
    speech_language_router.py) instead of silently defaulting to
    Gemini and producing a poor or wrong-language result.

    Two cases are distinguished:
    - A language that was supported before but has since been dropped
      (e.g. Khasi, Mizo) — named specifically, so it's clear this is a
      "not yet available" situation rather than a typo.
    - Any other unrecognized code — generic message listing what IS
      available, so the caller (app/patient) knows what to try instead.

    Args:
        language_code: The unsupported language code that was requested.
        include_emoji: If True, prefixes the message with a visual
            warning icon (see UNSUPPORTED_LANGUAGE_EMOJI) — use this for
            on-screen/app display, where a language-independent visual
            cue helps regardless of what language the patient/caregiver
            reads. Leave False for any message headed into
            text_to_speech.py for spoken output.
        message_language: "en" or "hi" — which language to write the
            message text in. Only these two are supported (see module
            note above on why the other 5 languages aren't translated).
            Falls back to "en" for any other value rather than raising,
            since a bad/missing app-language setting shouldn't itself
            crash the rejection message it's trying to display.
    """
    lang = message_language if message_language in ("en", "hi") else "en"

    if language_code in PREVIOUSLY_SUPPORTED_LANGUAGES:
        name = PREVIOUSLY_SUPPORTED_LANGUAGES[language_code]
        message = _UNSUPPORTED_TEMPLATES[lang].format(
            name=name, codes=", ".join(get_all_language_codes())
        )
    else:
        supported_names = ", ".join(
            f"{l.english_name} ({l.code})" for l in get_all_languages()
        )
        message = _UNKNOWN_CODE_TEMPLATES[lang].format(
            code=language_code, names=supported_names
        )

    if include_emoji:
        return f"{UNSUPPORTED_LANGUAGE_EMOJI} {message}"

    return message


# ---------------------------------------------------------
# Simple test
# ---------------------------------------------------------

if __name__ == "__main__":
    print("Supported languages:")
    print("=" * 65)

    for lang in get_all_languages():
        print(f"{lang.code:5} | {lang.english_name:10} | {lang.native_name:20} | {lang.provider}")

    print("\nProvider grouping:")
    print("=" * 65)
    print("Gemini:", [l.code for l in get_languages_by_provider(PROVIDER_GEMINI)])
    print("Regional API:", [l.code for l in get_languages_by_provider(PROVIDER_REGIONAL_API)])

    print("\nLookup tests:")
    print("=" * 65)
    print("is_supported('hi'):", is_supported("hi"))
    print("is_supported('fr'):", is_supported("fr"))
    print("get_provider('bn'):", get_provider("bn"))
    print("get_provider('as'):", get_provider("as"))
    print("uses_gemini('en'):", uses_gemini("en"))
    print("uses_regional_api('mni'):", uses_regional_api("mni"))
    print("get_language_name('mni'):", get_language_name("mni"))

    print("\nUnsupported language messages:")
    print("=" * 65)
    print("[Spoken/TTS — English]")
    print(get_unsupported_language_message("lus"))  # previously supported (Mizo)
    print(get_unsupported_language_message("fr"))  # never supported (French)

    print("\n[Spoken/TTS — Hindi]")
    print(get_unsupported_language_message("lus", message_language="hi"))
    print(get_unsupported_language_message("fr", message_language="hi"))

    print("\n[App/screen — English + emoji]")
    print(get_unsupported_language_message("kh", include_emoji=True))

    print("\n[App/screen — Hindi + emoji]")
    print(get_unsupported_language_message("kh", include_emoji=True, message_language="hi"))