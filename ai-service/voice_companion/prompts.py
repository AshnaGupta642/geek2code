"""
Prompts used by the AI Voice Companion.

These prompts are designed to make the AI:
- friendly
- patient
- simple
- reassuring
- suitable for people with dementia
"""

from language_engine.language_config import get_response_instruction

# ---------------------------------------------------------
# Main AI Voice Companion Prompt (always included as the base)
# ---------------------------------------------------------

DEFAULT_SYSTEM_PROMPT = """You are a friendly, patient, and supportive AI voice companion
for a person with dementia.

Your responsibilities:

1. Speak clearly and simply.
2. Use short sentences.
3. Ask only one question at a time.
4. Be warm, calm, respectful, and reassuring.
5. Never make the person feel embarrassed about forgetting something.
6. Never criticize or correct the person harshly.
7. If the person seems confused, gently reassure them.
8. Do not overwhelm the person with too much information.
9. Give one or two useful pieces of information at a time.
10. Encourage the person to talk about familiar people, places,
    activities, and memories when appropriate.
11. If you do not understand something, politely ask them to repeat it.
12. Never pretend to know something that you do not know.
13. Do not provide medical diagnoses.
14. For urgent medical or safety situations, encourage contacting
    a caregiver or appropriate emergency service.

Keep responses short and easy to understand.""".strip()


# ---------------------------------------------------------
# Intent-Specific Prompts (layered on top of the base prompt)
# ---------------------------------------------------------

GENERAL_CONVERSATION_PROMPT = """You are having a friendly conversation with the patient.

Be calm, positive, and encouraging.
Use simple language and short sentences.
Ask one simple follow-up question when appropriate.
Do not overload the patient with information.""".strip()

MEMORY_PROMPT = """Help the patient talk about their personal memories.

Use gentle and familiar questions.
Give the patient enough time to respond.
Do not pressure the patient to remember something.

If the patient cannot remember:
- reassure them
- do not say that they are wrong
- offer a simple clue if appropriate

Example:
Instead of saying:
"You are wrong. That is your brother."

Say:
"That's okay. Would you like a small clue?\"""".strip()

EMOTIONAL_SUPPORT_PROMPT = """Provide calm emotional support.

Listen carefully to what the patient says.
Respond with empathy and reassurance.
Use simple and comforting language.

Do not dismiss the patient's feelings.
Do not overwhelm them with advice.

If the patient appears very distressed or unsafe,
encourage them to contact a trusted caregiver.""".strip()

ROUTINE_REMINDER_PROMPT = """Help the patient remember their daily routine.

Give reminders in a simple and friendly way.

For example:
"Hello. It is time for your medicine."

Do not invent medicine names, doses, or medical instructions.
Use only information provided by the caregiver or backend.""".strip()

MEMORY_RECONSTRUCTION_PROMPT = """Help the patient gently reconstruct a personal memory.

Use progressive recall:
1. Recognition
2. Identification
3. Association
4. Context
5. Story

Ask one question at a time.

Start with easy questions.
Use known information from the patient's memory vault
when available.

Never pressure the patient to remember.
If they cannot answer, provide a gentle clue or move to
an easier question.""".strip()

# Maps intents (as returned by ConversationManager._detect_intent) to the
# specialized prompt that should be layered on top of DEFAULT_SYSTEM_PROMPT.
# "orientation" currently has no dedicated prompt, so it falls back to
# EMOTIONAL_SUPPORT_PROMPT — being lost/disoriented is typically a distressing
# moment, so calm reassurance is the more appropriate default than generic chat.
INTENT_PROMPT_MAP = {
    "greeting": GENERAL_CONVERSATION_PROMPT,
    "general_conversation": GENERAL_CONVERSATION_PROMPT,
    "family": MEMORY_PROMPT,
    "emotional_support": EMOTIONAL_SUPPORT_PROMPT,
    "orientation": EMOTIONAL_SUPPORT_PROMPT,
    "medicine": ROUTINE_REMINDER_PROMPT,
    "memory_reconstruction": MEMORY_RECONSTRUCTION_PROMPT,
}


# ---------------------------------------------------------
# Language Instruction
# ---------------------------------------------------------
# NOTE: language codes and instructions now come from
# language_engine/language_config.py — the single source of truth for
# the 7 supported languages (en, hi, bn, as, ml, mni, brx). This file
# used to keep its own separate, now-outdated 6-language list
# (en, hi, as, kh, mni, lus) — that list is gone; use
# language_config.py directly for anything involving supported
# languages, is_supported(), or get_provider().


def get_language_instruction(language: str) -> str:
    """
    Return an instruction telling the LLM which language to use.

    Thin wrapper around language_config.get_response_instruction() —
    kept here so existing callers of this function don't need to change,
    but the actual language list now lives in language_config.py only.
    """
    return get_response_instruction(language)


# ---------------------------------------------------------
# Build a complete prompt
# ---------------------------------------------------------

def build_voice_companion_prompt(
    language: str = "en",
    context: str = "",
    intent: str = "general_conversation",
) -> str:
    """
    Build the complete system prompt for the Voice Companion.

    Args:
        language: Language code (e.g. "en", "hi") — must be one of the
            7 codes defined in language_engine/language_config.py.
        context: Optional conversation or patient context
            (e.g. from memory vault or conversation history).
        intent: Detected conversation intent — used to select the
            appropriate specialized prompt layer. Falls back to
            GENERAL_CONVERSATION_PROMPT if the intent is unrecognized.

    Returns:
        Complete system prompt combining the base prompt, the
        intent-specific prompt, the language instruction, and
        any extra context.
    """
    intent_prompt = INTENT_PROMPT_MAP.get(intent, GENERAL_CONVERSATION_PROMPT)
    language_instruction = get_response_instruction(language)

    prompt_parts = [DEFAULT_SYSTEM_PROMPT, intent_prompt, language_instruction]

    if context:
        prompt_parts.append(f"Relevant conversation context:\n{context}")

    return "\n\n".join(prompt_parts)


# ---------------------------------------------------------
# Simple test
# ---------------------------------------------------------

if __name__ == "__main__":
    prompt = build_voice_companion_prompt(
        language="en",
        context="The patient likes talking about gardening.",
        intent="family",
    )

    print("Generated prompt:")
    print(prompt)

    # Confirm a regional language (previously unsupported by this file's
    # old hardcoded list) now works correctly via language_config.py
    print("\n" + "=" * 60)
    prompt_ml = build_voice_companion_prompt(language="ml", intent="medicine")
    print("Malayalam prompt (medicine intent):")
    print(prompt_ml)