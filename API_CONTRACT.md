Pasted code(20260908-111221).py
Python
Pasted code (2)(3).py
Python
Pasted code (3).py
Python
Pasted code (4).py
Python
Pasted code (5).py
Python
she send me the files i am sending you that """ 
Response Localizer 
 
Verifies that the AI's generated response is actually written in the 
language it was supposed to respond in, and corrects it if not, before 
it goes to text_to_speech.py. 
 
Why this exists: 
LLMs — including Gemini — don't always follow a "respond in X language" 
instruction perfectly, especially for languages they support less well 
(as we've already established: Bodo and, to a lesser extent, Manipuri 
and Assamese, are weaker/unconfirmed for Gemini). A common failure mode 
is the model drifting back to English mid-response, or ignoring the 
instruction entirely for a low-resource language. Speaking an English 
sentence to a patient who was supposed to hear Bodo is a real, silent 
failure that would otherwise go undetected until a person actually 
listens to the output. 
 
This module closes that gap: it detects the actual language of the 
generated response (reusing language_detector.py) and, if it doesn't 
match the intended target language, translates it into the correct 
language (reusing translator.py) before it's handed off to TTS. 
""" 
 
import logging 
from typing import Dict, Optional 
 
from .language_config import get_language_name, is_supported 
from .language_detector import LanguageDetector 
from .translator import Translator 
 
logger = logging.getLogger(__name__) 
 
# Only auto-correct when the mismatch was detected with high confidence. 
# A "low" confidence detection (e.g. an ambiguous script that fell back 
# to a guess) isn't a reliable enough signal to justify translating an 
# otherwise-correct response — that would risk introducing translation 
# errors into text that may have been fine to begin with. 
MIN_CONFIDENCE_TO_CORRECT = "high" 
 
 
class ResponseLocalizer: 
    """ 
    Confirms (and if needed, corrects) that a generated response is 
    actually in the intended target language before it's spoken aloud. 
    """ 
 
    def __init__( 
        self, 
        detector: Optional[LanguageDetector] = None, 
        translator: Optional[Translator] = None, 
    ) -> None: 
        self.detector = detector or LanguageDetector() 
        self.translator = translator or Translator() 
 
    # --------------------------------------------------------- 
    # Main entry point 
    # --------------------------------------------------------- 
 
    def localize(self, response_text: str, target_language: str) -> Dict[str, object]: 
        """ 
        Verify response_text is in target_language; correct it if not. 
 
        Args: 
            response_text: The AI-generated response (from llm_client.py), 
                which was supposed to be in target_language. 
            target_language: The language code the response was meant 
                to be in (e.g. what conversation_manager.py requested). 
 
        Returns: 
            { 
                "text": str,              # the final text to hand to TTS 
                "was_corrected": bool,    # True if a mismatch was fixed 
                "detected_language": str, # what language the original text was actually in 
                "target_language": str, 
                "detection_confidence": "high" | "low", 
                "note": str | None,       # set if correction was attempted but failed 
            } 
 
        Raises: 
            ValueError: If response_text is empty or target_language 
                is not one of the 7 supported languages. 
        """ 
        if not response_text or not response_text.strip(): 
            raise ValueError("response_text cannot be empty.") 
 
        if not is_supported(target_language): 
            raise ValueError(f"target_language '{target_language}' is not supported.") 
 
        detection = self.detector.detect_language(response_text) 
        detected_language = detection["language_code"] 
        detection_confidence = detection["confidence"] 
 
        result: Dict[str, object] = { 
            "text": response_text, 
            "was_corrected": False, 
            "detected_language": detected_language, 
            "target_language": target_language, 
            "detection_confidence": detection_confidence, 
            "note": None, 
        } 
 
        if detected_language == target_language: 
            return result 
 
        if detection_confidence != MIN_CONFIDENCE_TO_CORRECT: 
            logger.info( 
                "Response looked like it might not be in %s (detected %s), " 
                "but detection confidence was low — leaving response as-is " 
                "rather than risking an unnecessary translation.", 
                target_language, 
                detected_language, 
            ) 
            return result 
 
        logger.warning( 
            "AI response was generated in '%s' but should have been in '%s' " 
            "(%s). Attempting automatic correction via translation.", 
            get_language_name(detected_language), 
            get_language_name(target_language), 
            target_language, 
        ) 
 
        try: 
            translation = self.translator.translate( 
                text=response_text, 
                source_language=detected_language, 
                target_language=target_language, 
            ) 
            result["text"] = translation["translated_text"] 
            result["was_corrected"] = True 
            if translation["confidence"] == "low": 
                result["note"] = ( 
                    "Response was auto-corrected to the right language, but the " 
                    "correction itself used a lower-confidence translation path." 
                ) 
        except (ValueError, RuntimeError) as exc: 
            logger.error( 
                "Failed to auto-correct response language (%s -> %s): %s. " 
                "Speaking the original, wrong-language response rather than " 
                "failing the whole conversation turn.", 
                detected_language, 
                target_language, 
                exc, 
            ) 
            result["note"] = ( 
                f"Response may be in the wrong language ({get_language_name(detected_language)} " 
                f"instead of {get_language_name(target_language)}); automatic correction failed." 
            ) 
 
        return result 
 
 
# --------------------------------------------------------- 
# Simple test 
# --------------------------------------------------------- 
 
if __name__ == "__main__": 
    logging.basicConfig(level=logging.INFO) 
 
    localizer = ResponseLocalizer() 
 
    print("=" * 60) 
    print("Case 1 — response already in the correct language") 
    print("=" * 60) 
    result = localizer.localize("आप कैसे हैं?", target_language="hi") 
    print(result) 
 
    print("\n" + "=" * 60) 
    print("Case 2 — LLM drifted to English when Hindi was requested") 
    print("=" * 60) 
    result = localizer.localize( 
        "How are you feeling today?", target_language="hi" 
    ) 
    print(result) 
    print(f"\nCorrected: {result['was_corrected']}") 
    print(f"Final text: {result['text']}")  """ 
Context Manager for the AI Voice Companion. 
 
Stores recent conversation messages for each conversation_id. 
This helps the LLM maintain context across multiple turns. 
 
NOTE: This is in-memory storage only — all conversation history is 
lost if the process restarts, and it will NOT be shared across 
multiple server instances/workers. For production, Person 5's 
backend/database should be the source of truth for conversation 
history; this class is best used as a fast local cache layered 
on top of that, not a replacement for it. 
""" 
 
import threading 
from typing import Dict, List 
 
 
class ContextManager: 
    """Manage conversation history for voice companion sessions.""" 
 
    def __init__(self, max_messages: int = 10): 
        """ 
        Args: 
            max_messages: Maximum number of messages to keep 
                          for each conversation. Must be positive. 
        """ 
        if max_messages <= 0: 
            raise ValueError("max_messages must be a positive integer.") 
 
        self.max_messages = max_messages 
 
        # Example: 
        # { 
        #     "C001": [ 
        #         {"role": "user", "content": "Hello"}, 
        #         {"role": "assistant", "content": "Hello! How are you?"} 
        #     ] 
        # } 
        self.conversations: Dict[str, List[Dict[str, str]]] = {} 
        self._lock = threading.Lock() 
 
    # --------------------------------------------------------- 
    # Create a conversation 
    # --------------------------------------------------------- 
 
    def create_conversation(self, conversation_id: str) -> None: 
        """Create a new conversation if it does not already exist.""" 
        if not conversation_id: 
            raise ValueError("conversation_id is required") 
 
        with self._lock: 
            if conversation_id not in self.conversations: 
                self.conversations[conversation_id] = [] 
 
    # --------------------------------------------------------- 
    # Add a message 
    # --------------------------------------------------------- 
 
    def add_message( 
        self, 
        conversation_id: str, 
        role: str, 
        content: str, 
    ) -> None: 
        """ 
        Add a message to a conversation. 
 
        role should normally be: 
            user 
            assistant 
        """ 
        if not conversation_id: 
            raise ValueError("conversation_id is required") 
 
        if not content or not content.strip(): 
            raise ValueError("Message content cannot be empty") 
 
        if role not in {"user", "assistant", "system"}: 
            raise ValueError("role must be 'user', 'assistant', or 'system'") 
 
        with self._lock: 
            if conversation_id not in self.conversations: 
                self.conversations[conversation_id] = [] 
 
            self.conversations[conversation_id].append( 
                {"role": role, "content": content.strip()} 
            ) 
 
            # Keep only the most recent messages 
            history = self.conversations[conversation_id] 
            if len(history) > self.max_messages: 
                self.conversations[conversation_id] = history[-self.max_messages:] 
 
    # --------------------------------------------------------- 
    # Get conversation history 
    # --------------------------------------------------------- 
 
    def get_history(self, conversation_id: str) -> List[Dict[str, str]]: 
        """Return conversation history.""" 
        with self._lock: 
            return self.conversations.get(conversation_id, []).copy() 
 
    # --------------------------------------------------------- 
    # Get recent context as text 
    # --------------------------------------------------------- 
 
    def get_context(self, conversation_id: str) -> str: 
        """ 
        Convert conversation history into text that can 
        be given to the LLM. 
        """ 
        history = self.get_history(conversation_id) 
 
        if not history: 
            return "" 
 
        context_lines = [ 
            f"{message['role'].capitalize()}: {message['content']}" 
            for message in history 
        ] 
 
        return "\n".join(context_lines) 
 
    # --------------------------------------------------------- 
    # Clear conversation 
    # --------------------------------------------------------- 
 
    def clear_conversation(self, conversation_id: str) -> None: 
        """Delete all messages from a conversation.""" 
        with self._lock: 
            self.conversations.pop(conversation_id, None) 
 
    # --------------------------------------------------------- 
    # Check conversation 
    # --------------------------------------------------------- 
 
    def exists(self, conversation_id: str) -> bool: 
        """Check whether a conversation exists.""" 
        with self._lock: 
            return conversation_id in self.conversations 
 
    # --------------------------------------------------------- 
    # Number of messages 
    # --------------------------------------------------------- 
 
    def message_count(self, conversation_id: str) -> int: 
        """Return number of stored messages.""" 
        with self._lock: 
            return len(self.conversations.get(conversation_id, [])) 
 
 
# --------------------------------------------------------- 
# Simple test 
# --------------------------------------------------------- 
 
if __name__ == "__main__": 
    context_manager = ContextManager(max_messages=10) 
 
    conversation_id = "C001" 
 
    context_manager.add_message(conversation_id, "user", "Hello, my name is Rina.") 
    context_manager.add_message( 
        conversation_id, "assistant", "Hello Rina! It is nice to talk with you." 
    ) 
    context_manager.add_message(conversation_id, "user", "I like gardening.") 
 
    print("Conversation history:") 
    print(context_manager.get_history(conversation_id)) 
 
    print("\nLLM Context:") 
    print(context_manager.get_context(conversation_id))  import logging 
import os 
import time 
from typing import Optional 
 
from dotenv import load_dotenv 
from google import genai 
from google.genai import types 
from google.genai.errors import APIError 
 
from .prompts import build_voice_companion_prompt 
 
load_dotenv() 
 
logger = logging.getLogger(__name__) 
 
DEFAULT_MODEL = "gemini-3.6-flash" 
MAX_RETRIES = 3 
BASE_RETRY_DELAY = 2  # seconds; doubles each retry (2s, 4s, 8s) 
 
 
class LLMClient: 
    """Generate dementia-friendly responses using the Gemini API.""" 
 
    def __init__( 
        self, 
        model: str = DEFAULT_MODEL, 
        api_key: Optional[str] = None, 
        system_prompt: Optional[str] = None, 
        temperature: float = 0.6, 
        max_retries: int = MAX_RETRIES, 
    ): 
        api_key = api_key or os.getenv("GEMINI_API_KEY") 
        if not api_key: 
            raise ValueError("GEMINI_API_KEY is not set. Check your .env file.") 
 
        self.model = model 
        # Falls back to the default voice-companion prompt (English, 
        # general_conversation intent, no extra context) if none is given. 
        # Callers that know the language/intent/context (e.g. 
        # ConversationManager) should build their own prompt with 
        # build_voice_companion_prompt() and pass it into generate_response(). 
        self.system_prompt = system_prompt or build_voice_companion_prompt() 
        self.temperature = temperature 
        self.max_retries = max_retries 
        self.client = genai.Client(api_key=api_key) 
 
    def generate_response( 
        self, 
        user_text: str, 
        system_prompt: Optional[str] = None, 
    ) -> str: 
        """ 
        Generate an AI response from the patient's text. 
 
        Args: 
            user_text: Text received from speech-to-text. 
            system_prompt: Optional override for this call's instructions. 
                Typically built via prompts.build_voice_companion_prompt() 
                with the correct language/intent/context. Falls back to 
                the instance's default system_prompt if not provided. 
 
        Returns: 
            AI-generated response text. 
 
        Raises: 
            ValueError: If user_text is empty. 
            RuntimeError: If the API call fails after all retries, or returns nothing. 
        """ 
        if not user_text or not user_text.strip(): 
            raise ValueError("user_text cannot be empty.") 
 
        active_system_prompt = system_prompt or self.system_prompt 
 
        logger.info("Generating LLM response using model=%s", self.model) 
 
        response = None 
        last_error: Optional[APIError] = None 
 
        for attempt in range(1, self.max_retries + 1): 
            try: 
                response = self.client.models.generate_content( 
                    model=self.model, 
                    contents=user_text.strip(), 
                    config=types.GenerateContentConfig( 
                        system_instruction=active_system_prompt, 
                        temperature=self.temperature, 
                    ), 
                ) 
                break 
            except APIError as exc: 
                last_error = exc 
                is_last_attempt = attempt == self.max_retries 
 
                if is_last_attempt: 
                    logger.exception( 
                        "LLM request failed after %d attempts", self.max_retries 
                    ) 
                    raise RuntimeError(f"LLM request failed: {exc}") from exc 
 
                wait_seconds = BASE_RETRY_DELAY * (2 ** (attempt - 1)) 
                logger.warning( 
                    "LLM request attempt %d/%d failed (%s). Retrying in %ds...", 
                    attempt, 
                    self.max_retries, 
                    exc, 
                    wait_seconds, 
                ) 
                time.sleep(wait_seconds) 
 
        response_text = (response.text or "").strip() if response else "" 
        if not response_text: 
            raise RuntimeError("LLM returned an empty response.") 
 
        return response_text 
 
 
if __name__ == "__main__": 
    logging.basicConfig(level=logging.INFO) 
 
    llm = LLMClient() 
 
    try: 
        user_text = input("Patient: ") 
        result = llm.generate_response(user_text) 
        print("\nAI Companion:") 
        print(result) 
    except (ValueError, RuntimeError) as err: 
        print(f"Error: {err}") """ 
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
    print(prompt_ml) import logging 
import os 
from pathlib import Path 
from typing import Optional 
 
from dotenv import load_dotenv 
from google import genai 
from google.genai import types 
from google.genai.errors import APIError 
 
load_dotenv() 
 
logger = logging.getLogger(__name__) 
 
SUPPORTED_FORMATS = {".wav", ".mp3", ".m4a", ".mp4", ".mpeg", ".mpga", ".webm"} 
DEFAULT_MODEL = "gemini-3.5-transcribe" 
 
MIME_TYPES = { 
    ".wav": "audio/wav", 
    ".mp3": "audio/mp3", 
    ".m4a": "audio/mp4", 
    ".mp4": "audio/mp4", 
    ".mpeg": "audio/mpeg", 
    ".mpga": "audio/mpeg", 
    ".webm": "audio/webm", 
} 
 
 
class SpeechToText: 
    """Convert patient's voice/audio into text using the Gemini API.""" 
 
    def __init__(self, model: str = DEFAULT_MODEL, api_key: Optional[str] = None): 
        api_key = api_key or os.getenv("GEMINI_API_KEY") 
        if not api_key: 
            raise ValueError("GEMINI_API_KEY is not set (check your .env file).") 
 
        self.model = model 
        self.client = genai.Client(api_key=api_key) 
 
    @staticmethod 
    def _validate_audio(path: Path) -> None: 
        if not path.exists(): 
            raise FileNotFoundError(f"Audio file not found: {path}") 
        if not path.is_file(): 
            raise ValueError(f"Path is not a file: {path}") 
        if path.suffix.lower() not in SUPPORTED_FORMATS: 
            raise ValueError( 
                f"Unsupported audio format '{path.suffix}'. " 
                f"Supported: {', '.join(sorted(SUPPORTED_FORMATS))}" 
            ) 
        if path.stat().st_size == 0: 
            raise ValueError(f"Audio file is empty: {path}") 
 
    def transcribe( 
        self, 
        audio_path: str, 
        language: Optional[str] = None, 
        prompt: Optional[str] = None, 
    ) -> str: 
        """ 
        Convert an audio file into text. 
 
        Args: 
            audio_path: Path to the audio file. 
            language: Optional language name/code hint, e.g. "en" or "hi". 
                gemini-3.5-transcribe auto-detects language, but this can help. 
            prompt: Optional context/vocabulary hint (e.g. medical terms, names). 
 
        Returns: 
            Transcribed text. 
 
        Raises: 
            FileNotFoundError: If the audio file doesn't exist. 
            ValueError: If the file is invalid or unsupported. 
            RuntimeError: If the API call fails. 
        """ 
        path = Path(audio_path) 
        self._validate_audio(path) 
 
        mime_type = MIME_TYPES.get(path.suffix.lower(), "audio/mpeg") 
 
        logger.info("Transcribing %s (model=%s, language=%s)", path, self.model, language) 
 
        try: 
            uploaded_file = self.client.files.upload( 
                file=str(path), 
                config=types.UploadFileConfig(mime_type=mime_type), 
            ) 
 
            input_parts = [ 
                { 
                    "type": "audio", 
                    "uri": uploaded_file.uri, 
                    "mime_type": uploaded_file.mime_type, 
                } 
            ] 
 
            interaction = self.client.interactions.create( 
                model=self.model, 
                input=input_parts, 
            ) 
        except APIError as exc: 
            logger.exception("Transcription failed for %s", path) 
            raise RuntimeError(f"Transcription failed: {exc}") from exc 
 
        text = (interaction.output_text or "").strip() 
        if not text: 
            logger.warning("Transcription returned empty text for %s", path) 
 
        return text 
 
 
if __name__ == "__main__": 
    logging.basicConfig(level=logging.INFO) 
 
    stt = SpeechToText() 
 
    try: 
        result = stt.transcribe(audio_path="sample_audio.wav", language="en") 
        print("Transcription:") 
        print(result) 
    except (FileNotFoundError, ValueError, RuntimeError) as err: 
        print(f"Error: {err}") import logging 
import os 
import wave 
from pathlib import Path 
from typing import Optional 
 
from dotenv import load_dotenv 
from google import genai 
from google.genai import types 
from google.genai.errors import APIError 
 
load_dotenv() 
 
logger = logging.getLogger(__name__) 
 
DEFAULT_MODEL = "gemini-3.1-flash-tts-preview" 
DEFAULT_VOICE = "Kore" 
 
# Gemini's native TTS output format (per API docs) 
PCM_SAMPLE_RATE = 24000 
PCM_SAMPLE_WIDTH_BYTES = 2  # 16-bit 
PCM_CHANNELS = 1  # mono 
 
OUTPUT_DIR = Path(__file__).parent.parent / "data" / "audio_responses" 
OUTPUT_DIR.mkdir(parents=True, exist_ok=True) 
 
 
class TextToSpeech: 
    """Convert AI-generated text into speech using the Gemini API.""" 
 
    def __init__( 
        self, 
        model: str = DEFAULT_MODEL, 
        voice: str = DEFAULT_VOICE, 
        api_key: Optional[str] = None, 
    ): 
        api_key = api_key or os.getenv("GEMINI_API_KEY") 
        if not api_key: 
            raise ValueError("GEMINI_API_KEY is not set. Check your .env file.") 
 
        self.model = model 
        self.voice = voice 
        self.client = genai.Client(api_key=api_key) 
 
    def synthesize( 
        self, 
        text: str, 
        output_path: Optional[str] = None, 
    ) -> str: 
        """ 
        Convert text into speech and save it as a playable WAV file. 
 
        Args: 
            text: Text that should be spoken. 
            output_path: Optional path for the generated audio file. 
 
        Returns: 
            Path to the generated audio file. 
 
        Raises: 
            ValueError: If text is empty. 
            RuntimeError: If the Gemini API call fails or returns no audio. 
        """ 
        if not text or not text.strip(): 
            raise ValueError("text cannot be empty.") 
 
        if output_path is None: 
            output_path = str(OUTPUT_DIR / "response.wav") 
 
        output_file = Path(output_path) 
        output_file.parent.mkdir(parents=True, exist_ok=True) 
 
        logger.info("Generating speech using model=%s, voice=%s", self.model, self.voice) 
 
        try: 
            response = self.client.models.generate_content( 
                model=self.model, 
                contents=text.strip(), 
                config=types.GenerateContentConfig( 
                    response_modalities=["AUDIO"], 
                    speech_config=types.SpeechConfig( 
                        voice_config=types.VoiceConfig( 
                            prebuilt_voice_config=types.PrebuiltVoiceConfig( 
                                voice_name=self.voice 
                            ) 
                        ) 
                    ), 
                ), 
            ) 
        except APIError as exc: 
            logger.exception("Text-to-speech request failed") 
            raise RuntimeError(f"Text-to-speech request failed: {exc}") from exc 
 
        try: 
            pcm_data = response.candidates[0].content.parts[0].inline_data.data 
            if not pcm_data: 
                raise ValueError("Empty audio payload") 
        except (AttributeError, IndexError, TypeError, ValueError) as exc: 
            logger.exception("No audio data returned by Gemini") 
            raise RuntimeError("Gemini returned no usable audio data.") from exc 
 
        # Gemini returns raw PCM — wrap it in a proper WAV header before saving. 
        with wave.open(str(output_file), "wb") as wav_file: 
            wav_file.setnchannels(PCM_CHANNELS) 
            wav_file.setsampwidth(PCM_SAMPLE_WIDTH_BYTES) 
            wav_file.setframerate(PCM_SAMPLE_RATE) 
            wav_file.writeframes(pcm_data) 
 
        logger.info("Audio saved to %s", output_file) 
        return str(output_file) 
 
 
if __name__ == "__main__": 
    logging.basicConfig(level=logging.INFO) 
 
    tts = TextToSpeech() 
 
    try: 
        text = input("AI response: ") 
        output = tts.synthesize( 
            text=text, 
            output_path=str(OUTPUT_DIR / "test_response.wav"), 
        ) 
        print("\nAudio generated successfully:") 
        print(output) 
    except (ValueError, RuntimeError) as err: 
        print(f"Error: {err}") 
Pasted text(20260908-112030).txt
Document
Pasted text (2)(2).txt
Document

Aha, ab exact problem mil gaya. Your FamilyMember model does not have caregiver_id.

It has:

patient_id
user_id
is_caregiver

So my previous code was wrong here:

FamilyMember.caregiver_id == caregiver.id
But there's an even simpler fix

For your project, caregiver_id = 3 appears to be a FamilyMember ID, not a Caregiver.id.

So we should validate it directly through FamilyMember.

Replace backend/app/api/personalized_voice.py

Use this complete version:

import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.core.dependencies import get_current_user

from app.models.patient import Patient
from app.models.family_member import FamilyMember

from app.schemas.personalized_voice import (
    PersonalizedVoiceRequest,
    PersonalizedVoiceResponse
)

from app.services.personalized_voice_service import (
    PersonalizedVoiceService
)


router = APIRouter(
    prefix="/api/personalized-voice",
    tags=["Personalized Voice"]
)

voice_service = PersonalizedVoiceService()


@router.post(
    "/process",
    response_model=PersonalizedVoiceResponse
)
def process_personalized_voice(
    request: PersonalizedVoiceRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    # Verify patient
    patient = (
        db.query(Patient)
        .filter(Patient.id == request.patient_id)
        .first()
    )

    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )

    # Verify that current user owns this patient
    if patient.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized for this patient"
        )

    # Verify family member / caregiver
    family_member = (
        db.query(FamilyMember)
        .filter(
            FamilyMember.id == request.caregiver_id,
            FamilyMember.patient_id == patient.id,
            FamilyMember.is_caregiver == True,
            FamilyMember.is_active == True
        )
        .first()
    )

    if not family_member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Caregiver not found or not linked to this patient"
        )

    voice_recording_id = str(uuid.uuid4())

    try:
        result = voice_service.process_voice(
            patient_id=patient.id,
            caregiver_id=family_member.id,
            audio_url=request.audio_url,
            reminder_type=request.reminder_type,
            reminder_text=request.reminder_text
        )

        result["voice_recording_id"] = voice_recording_id
        result["patient_id"] = patient.id
        result["caregiver_id"] = family_member.id

        return result

    except NotImplementedError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(e)
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
Then restart
python -m uvicorn app.main:app --reload

Test with:

{
  "patient_id": 2,
  "caregiver_id": 3,
  "audio_url": "/audio/example.wav",
  "reminder_type": "medicine",
  "reminder_text": "Mummy, please take your medicine."
}
Expected response

If FamilyMember 3 has:

patient_id = 2
is_caregiver = true
is_active = true

then you should reach the service and get:

{
  "detail": "Personalized Voice AI service is not connected yet."
}

That response is what we want at this stage. ✅

One important point: your project models use FamilyMember as the caregiver relationship, so we should not use Caregiver.id for this endpoint.

{   "detail": "Personalized Voice AI service is not connected yet." }  

Perfect. This is exactly the expected result. ✅

It means:

Patient 2 exists ✅
Caregiver/FamilyMember 3 is correctly linked to patient 2 ✅
Authentication/authorization passed ✅
Personalized Voice API is working ✅
Backend successfully reached the PersonalizedVoiceService ✅
Only the actual AI voice processing is pending — Person 4 will connect her Bhashini/AI code here.

So Personalized Voice backend integration is DONE. 🎉

Current Member 5 progress
Backend module	Status
Authentication/JWT	✅
PostgreSQL	✅
Memories	✅
Voice recordings/audio upload	✅
Reminders/medicine	✅
Notifications	✅
Caregiver APIs	✅
Activity/events	✅
Alerts	✅
Emergency	✅
Location/Safe Zones	✅
Offline Sync	✅
AI Voice API	✅ Ready for Person 4
Personal Memory Vault API	✅ Ready for AI member
Memory Graph API	✅ Ready for AI member
Memory Reconstruction API	✅ Ready for AI member
Personalized Voice API	✅ Ready for Person 4

Next step should be the final backend audit—checking main.py, all routers, model imports, route conflicts, and anything missing before you push your Member 5 work to GitHub.

Pasted markdown(5).md
File
i thinkits done update my api_contract.md 

Yes — ab tumhara backend side complete hai, so I updated the API_CONTRACT.md accordingly.

I added:

✅ AI Voice Companion API
✅ Personal Memory Vault API
✅ Memory Graph API
✅ Memory Reconstruction Start + Answer APIs
✅ Personalized Voice API
✅ AI language list: en, hi, as, kh, mni, lus
✅ Clear note that AI members integrate their own AI logic
✅ Current 503 service not connected status
✅ Corrected audio upload endpoint
✅ Clarified that caregiver_id is the linked FamilyMember caregiver ID

The existing document already contains the main backend/API map and integration rules.

Updated file

Download updated API_CONTRACT.md

Replace your current root API_CONTRACT.md with this one.

After this, your next step is GitHub push + give each member their API section.

API_CONTRACT_updated.md
Document

Library
/
API_CONTRACT_updated.md

Wednesday 12:45 PM

Pasted markdown(4).md

File

AI-Based Cognitive Gaming & Personal Memory Assistance Platform for Elderly Dementia Patients in NER

👴 Patient-Side Features — Priority Order

🧠 Personal Memory Vault – Patients can record their life experiences, memories and stories through voice, with photos, people, places and events linked to each memory.

🧩 Memory Reconstruction Engine – Breaks personal memories into interconnected elements and uses progressive, voice-based recall prompts to help patients reconstruct and engage with their own life stories.

🎙️ Voice-First AI Companion – The entire patient-side platform can be operated primarily through natural voice commands instead of complicated menus or typing.

🎮 AI-Adaptive Cognitive Games – Automatically adapts game type and difficulty based on the patient's previous performance and engagement.

👨‍👩‍👧 Face–Name & Relationship Association – Uses family photos, names, relationships and familiar voices to create personalized recognition and recall activities.

🗣️ Multilingual & Regional Voice Support – Voice interaction in Assamese, Khasi, Manipuri, Mizo, Hindi and English, with culturally familiar content for NER users.

📅 Personalized Daily Orientation – Voice-based information about day, date, time, weather, location, upcoming activities and personalized routine.

💊 Medicine & Routine Reminders – Voice reminders for medicines, hydration, meals, appointments and daily activities.

❤️ Personalized Family Voice Reminders – Caregivers/family members can record reminders in their own voice, e.g., “Mummy, please take your medicine now.”

🧩 Personalized Memory Games & Puzzles – Photo matching, sequence recall, patterns, jigsaw puzzles, object recognition and activities generated using the patient's own memories.

🎵 Music & Sound Memory Activities – Uses familiar songs, sounds and patient-approved audio to create personalized memory and recognition activities.

🏠 Safe Return Home – GPS-based location assistance with simple voice-guided navigation when a patient has difficulty finding their way home.

🚨 Emergency SOS – Voice command or one-tap emergency alert to notify registered caregivers.

📍 Live / Last Location Sharing – Consent-based location sharing with caregivers and configurable safe-zone alerts.

📴 Offline-First Mode – Core games, saved memories, reminders and essential voice functions continue working without internet, with synchronization when connectivity returns.

👨‍👩‍👧 Caregiver Side — Priority Order

📊 AI-Powered Caregiver Dashboard – Central dashboard showing the patient's daily activity, cognitive-engagement trends, routines, reminders and alerts.

🧠 Cognitive Engagement Analytics – Tracks performance across different activities and identifies areas of stronger/weaker engagement over time without claiming medical diagnosis.

💊 Medicine & Routine Adherence – Shows completed/missed medicines, hydration and scheduled activities.

🎙️ Remote Voice & Reminder Management – Caregivers can remotely create reminders, upload family voices and configure patient routines.

🚨 Caregiver Alerts – Notifications for SOS, missed important routines, safe-zone exits and other configured events.

📍 Location Monitoring – Current/last known location and configurable safety-zone monitoring.

🔐 Personal Memory & Access Control – Caregivers can add, verify, categorize and control access to patient memories, photos and voice recordings. i am doing person 5 work how to start and tell me how to tell which person to connect with me and i will set up the repo and everything tell me how to begin i am the wall i have to connect everythingmake it easier for me pls

PERSON 3 — AI, Voice & Memory Reconstruction What I Need From Other Team Members Person Their Responsibility What I Need From Them Why I Need It Person 1 Flutter Patient App Patient audio, patient_id, selected language, patient answers, photos/audio uploaded by patient To process voice, communicate with the AI, and create/reconstruct memories Person 2 Cognitive Games Game type, score, accuracy, time taken, difficulty level, date/time Optional: AI can use performance as patient context and provide personalized encouragement Person 4 GPS, Safety, Face Recognition Current/last location, SOS status, recognized person's name/ID AI can respond appropriately when a patient is lost or connect recognized family members with memories Person 5 Backend + Database APIs, database storage, patient profile, memories, conversation history, audio/photo storage MOST IMPORTANT: My AI needs data from the database and needs a way to save its results Person 6 Caregiver Dashboard Family member information, caregiver-created memories, photos, memory descriptions, recorded stories/corrections Provides the personal memory data used by the Memory Vault and Reconstruction Engine Data Flow Feature Input I Receive Output I Return AI Voice Companion Patient audio, patient_id, language Transcript, AI response text, TTS audio Personal Memory Vault Voice story/text, photos, patient ID Extracted people, places, events, dates, emotions Memory Graph Structured memory elements Relationships between people, places, events and memories Memory Reconstruction Memory ID, patient answer, previous context Next personalized recall question, updated memory state Regional Language AI Audio/text + selected language Response in the patient's language Personalized Voice Caregiver voice recording + reminder information Processed audio ready for storage/playback My 3 Main Dependencies Priority Person Why 1 Person 5 Backend, database, APIs and storage 2 Person 1 Patient voice/audio and AI interaction 3 Person 6 Family and personal memory information Final note: Person 4 is needed for safety, GPS and face-recognition integration, while Person 2's game-performance data is optional for the initial AI module. is this you wanted or i should ask him more specifically

a8a5b12b-8086-426a-a443-477532f0b55a.pdf

PDF

person 2 and 4 ke liye bhi ye docs bana do

{

  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwicm9sZSI6InBhdGllbnQiLCJleHAiOjE3ODgzNjQwMzZ9.HL0am9ezEgl_LYPoYfqNlxKnpNVT-qxEk1VrsllQSQk",

  "token_type": "bearer",

  "user_id": 1,

  "role": "patient"

}

👍

Pasted code(20260903-164930).py

Python

POST /api/reminders/event → Try it out i can't see this

👍

Pasted code(20260903-173548).py

Python

from datetime import datetime, timezone

from sqlalchemy import ForeignKey, String, DateTime, Float, Integer

from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base




class GameResult(Base):

    __tablename__ = "game_results"

    id: Mapped[int] = mapped_column(

        primary_key=True,

        index=True

    )

    session_id: Mapped[str] = mapped_column(

        ForeignKey("game_sessions.session_id"),

        nullable=False,

        index=True

    )

    patient_id: Mapped[int] = mapped_column(

        ForeignKey("patients.id"),

        nullable=False,

        index=True

    )

    game_id: Mapped[str] = mapped_column(

        ForeignKey("games.game_id"),

        nullable=False,

        index=True

    )

    score: Mapped[float] = mapped_column(

        Float,

        nullable=False

    )

    accuracy: Mapped[float] = mapped_column(

        Float,

        nullable=False

    )

    mistakes: Mapped[int] = mapped_column(

        Integer,

        default=0,

        nullable=False

    )

    duration_seconds: Mapped[int] = mapped_column(

        Integer,

        nullable=False

    )

    attempts: Mapped[int] = mapped_column(

        Integer,

        default=1,

        nullable=False

    )

    hints_used: Mapped[int] = mapped_column(

        Integer,

        default=0,

        nullable=False

    )

    response_time: Mapped[float | None] = mapped_column(

        Float,

        nullable=True

    )

    difficulty: Mapped[str] = mapped_column(

        String(20),

        nullable=False

    )

    completed_at: Mapped[datetime] = mapped_column(

        DateTime(timezone=True),

        nullable=False

    )

    created_at: Mapped[datetime] = mapped_column(

        DateTime(timezone=True),

        default=lambda: datetime.now(timezone.utc),

        nullable=False

    ) from datetime import datetime, timezone

from sqlalchemy import ForeignKey, String, DateTime

from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base




class GameSession(Base):

    __tablename__ = "game_sessions"

    id: Mapped[int] = mapped_column(

        primary_key=True,

        index=True

    )

    session_id: Mapped[str] = mapped_column(

        String(100),

        unique=True,

        nullable=False,

        index=True

    )

    patient_id: Mapped[int] = mapped_column(

        ForeignKey("patients.id"),

        nullable=False,

        index=True

    )

    game_id: Mapped[str] = mapped_column(

        ForeignKey("games.game_id"),

        nullable=False,

        index=True

    )

    difficulty: Mapped[str] = mapped_column(

        String(20),

        nullable=False

    )

    status: Mapped[str] = mapped_column(

        String(20),

        default="STARTED",

        nullable=False

    )

    started_at: Mapped[datetime] = mapped_column(

        DateTime(timezone=True),

        default=lambda: datetime.now(timezone.utc),

        nullable=False

    )

    completed_at: Mapped[datetime | None] = mapped_column(

        DateTime(timezone=True),

        nullable=True

    )  

👍

i can't find it

👍

Pasted code(20260903-180223).py

Python

POST /api/reminder-history/   ye nhi mill raha

👍

pakka ye mera kaam hai person1 ka nhi

👍

Haan, ye tumhara local backend URL hai:

http://127.0.0.1:8000

Toh tumhare liye Swagger:

http://127.0.0.1:8000/docs

⚠️ But team ko ye URL directly dene se kaam nahi karega

127.0.0.1 ka matlab "jis computer par request bheji ja rahi hai, wahi computer".

So agar Person 1 apne laptop se:

http://127.0.0.1:8000/api/memories/

hit karega, woh uske laptop ka backend dhoondhega, tumhara nahi.

Abhi development ke liye

Tum backend chala kar apne network ka IP use kar sakti ho:

http://YOUR_LOCAL_IP:8000

For example:

http://192.168.1.5:8000

Phir same Wi-Fi/network par connected team members use kar sakte hain.

Final integration ke liye

Best hai backend ko deploy karke ek common URL bana do:

https://memora-backend-xxxxx.com

Then everyone uses:

BASE_URL/api/...

and Swagger:

BASE_URL/docs

Abhi tum mujhe batao: kya tum sabko same Wi-Fi par connect karke integration karwaogi, ya backend ko internet par deploy karna hai? Uske according main exact next steps de dungi.

abhi mujhe batao mei ky kya karu jisse woh integration aasani se kar paaye

👍

Haan. Abhi tumhe unke integration ke liye backend side par ek proper handoff ready karna hai. Tumhara backend already working hai, so unnecessary code changes mat karo.

Abhi ye 6 kaam karo — isi order mein

1. Backend ko clean state mein rakho

Project structure roughly:

memora/

└── backend/

    ├── app/

    ├── uploads/

    ├── .env

    ├── requirements.txt

    └── ...

Ensure backend starts with:

uvicorn app.main:app --reload

and:

http://127.0.0.1:8000/docs

opens properly.

2. .gitignore check karo — VERY IMPORTANT

Backend GitHub par push karne se pehle:

.env

__pycache__/

*.pyc

.venv/

venv/

uploads/

firebase-service-account.json

.env kabhi GitHub par mat push karna.

3. requirements.txt updated rakho

Team member jab backend clone kare to:

pip install -r requirements.txt

se dependencies install ho jaani chahiye.

Tumhe unhe manually 10 packages ki list bhejne ki zarurat nahi honi chahiye.

4. Sabse important — API_CONTRACT.md banao

Backend repo ke root mein:

memora/

├── backend/

├── API_CONTRACT.md   ← NEW

├── README.md

└── ...

Is file mein har member ke liye:

Endpoint

Method

Authentication

Request body

Response

Purpose

likho.

Tumhare existing Swagger se ye information already available hai.

5. Team ko exact API mapping do

Ek simple document/message:

MEMORA BACKEND API HANDOFF

Base URL:

http://127.0.0.1:8000

Swagger:

http://127.0.0.1:8000/docs

Authentication:

Authorization: Bearer <JWT_TOKEN>

Then:

PERSON 1

Memory + Voice

→ /api/memories/

→ /api/voice-recordings/

→ /api/audio-upload/

PERSON 2

Games

→ /api/games/

→ /api/games/start

→ /api/games/result

→ /api/games/patient/{patient_id}

PERSON 3

AI/Cognitive

→ game performance

→ activity

→ memory data

PERSON 4

Safety

→ /api/location/

→ /api/safe-zones/

→ /api/emergency/sos

PERSON 6

Caregiver Dashboard

→ caregiver overview

→ activity

→ alerts

→ notifications

→ game performance

→ location

6. Unhe sample request + response bhi do

Ye integration ko bahut easy bana dega.

For example Person 2 ko:

POST /api/games/start

ka actual request aur actual response do.

Person 1 ko memory + audio ka example.

Person 4 ko location + SOS example.

Person 6 ko caregiver overview + notifications example.

Isse unhe Swagger mein baar-baar guess nahi karna padega.

⚠️ Ek problem abhi bhi hai: 127.0.0.1

Ye sirf tumhare laptop ke liye hai.

Agar team members alag laptops par hain, unko ye:

http://127.0.0.1:8000

mat dena.

Easiest temporary solution

Tum apna local IP nikaalo:

ipconfig

Usme IPv4 Address dekho.

Example:

192.168.1.7

Phir backend ko:

uvicorn app.main:app --host 0.0.0.0 --port 8000

se run karo.

Team same Wi-Fi par ho to woh use kar sakte hain:

http://192.168.1.7:8000/docs

Aur API base:

http://192.168.1.7:8000

Tumhare liye abhi exact checklist

☐ Backend starts without errors

☐ Swagger works

☐ requirements.txt updated

☐ .gitignore updated

☐ .env NOT pushed

☐ API_CONTRACT.md created

☐ Sample requests/responses documented

☐ GitHub push

☐ Local IP / deployed URL arrange

☐ Each member gets only the APIs they need

Aur ek important rule

Tum unke frontend/AI code mein integration mat karo.

Unka process:

Their Module

     ↓

Your API

     ↓

PostgreSQL

Agar Person 2 bole:

"Mujhe game result submit karne ke liye difficulty field bhi chahiye."

Tab woh requirement tumhe dega → tum backend API modify karogi.

Lekin tum uska game code connect nahi karogi.

Ab tumhara next best step API_CONTRACT.md banana hai. Main tumhare existing Memora backend ke saare endpoints ke according

ready-to-copy API_CONTRACT.md ka complete content bana sakti hoon, member-wise, with request/response examples.

API_CONTRACT.md ye banao

👍

Done. Maine complete API_CONTRACT.md bana diya hai, member-wise APIs, authentication, sample requests, integration rules, reminders, notifications, sync, etc. ke saath.

Download API_CONTRACT.md

Isko apne Memora repo ke root mein rakh do:

memora/

├── backend/

├── patient-app/

├── caregiver-dashboard/

├── ai-service/

├── game-engine/

├── safety-service/

├── API_CONTRACT.md   ← ye

└── README.md

Ab team members ko ye file + Swagger URL dena enough hoga.

API_CONTRACT.md

Document

Library

/

API_CONTRACT.md

MEMORA — API CONTRACT

1. Backend Information

Project: Memora

Backend: FastAPI

Database: PostgreSQL

Authentication: JWT Bearer Token

Local development

Base URL:

http://127.0.0.1:8000

Swagger:

http://127.0.0.1:8000/docs

127.0.0.1 works only when the backend is running on the same computer.

For team integration, use a shared/deployed backend URL or the host machine's local IP.

2. Authentication

Protected APIs require:

Authorization: Bearer <JWT_TOKEN>

Typical flow:

Register

   ↓

POST /api/auth/register

   ↓

Login

   ↓

POST /api/auth/login

   ↓

JWT token

   ↓

Use token in protected APIs

Do not commit JWT tokens or .env secrets to GitHub.

3. API Conventions

JSON is used for normal request/response bodies.

Audio upload uses multipart/form-data.

IDs are integers unless explicitly documented otherwise.

Game sessions use UUID-style session IDs.

Authentication and ownership are checked by the backend.

Do not connect directly to PostgreSQL from frontend/mobile applications.

Each module communicates through FastAPI APIs.

Swagger is the source of truth for the exact current request/response schema.

4. MEMBER 1 — Memories & Voice

Create Memory

POST /api/memories/

Auth: Patient

Example:

{

  "title": "My Wedding Day",

  "story_text": "A memory from my wedding day.",

  "summary": "Wedding day memory",

  "memory_type": "family",

  "tags": "wedding,family",

  "people": "Daughter,Husband",

  "event_date": "1995-05-20",

  "location": "Delhi",

  "cover_photo_url": "/images/wedding.jpg",

  "audio_url": null,

  "is_private": false

}

The backend controls is_approved; clients should not approve memories directly.

Get Memories

GET /api/memories/

Auth: Patient

Get One Memory

GET /api/memories/{memory_id}

Auth: Patient

Update Memory

PUT /api/memories/{memory_id}

Auth: Patient

Delete Memory

DELETE /api/memories/{memory_id}

Auth: Patient

Upload Audio

POST /api/audio/upload

Auth: Patient

This endpoint accepts multipart/form-data and stores the uploaded audio.

Content-Type: multipart/form-data

Supported formats:

MP3, WAV, M4A, OGG

Maximum file size: 10 MB.

The upload API stores the audio and creates the voice-recording information.

Create Voice Recording

POST /api/voice-recordings/

Auth: Patient

Example:

{

  "memory_id": 2,

  "family_member_id": 5,

  "audio_url": "/audio/wedding_memory.mp3",

  "language": "hi",

  "recording_type": "MEMORY_STORY",

  "duration_seconds": 45

}

Get Patient Voice Recordings

GET /api/voice-recordings/

Auth: Patient

Get One Voice Recording

GET /api/voice-recordings/{recording_id}

Auth: Patient

Caregiver Voice Recordings

GET /api/voice-recordings/caregiver/{patient_id}

Auth: Authorized caregiver

5. MEMBER 2 — Cognitive Games

Get Active Games

GET /api/games/

Get Game Details

GET /api/games/{game_id}

Start Game

POST /api/games/start

Auth: Patient

Example:

{

  "game_id": 1

}

The response contains a session_id. Store it and use it when submitting the game result.

Submit Game Result

POST /api/games/result

Auth: Patient

The result must reference the game session created by /api/games/start.

The backend:

validates session ownership

stores the result

completes the session

calculates the next difficulty using the current backend rule

Use Swagger for the exact current request schema.

Patient Game Data

GET /api/games/patient/{patient_id}

Caregiver Game Performance

GET /api/games/performance/{patient_id}

Auth: Caregiver

Game Performance Trend

GET /api/games/performance/{patient_id}/trend

Auth: Caregiver

6. MEMBER 3 — AI / Cognitive Analysis

The AI module should consume backend data through APIs instead of accessing PostgreSQL directly.

Useful endpoints:

GET /api/games/performance/{patient_id}

GET /api/games/performance/{patient_id}/trend

GET /api/caregiver/patients/{patient_id}/activity

GET /api/memories/

GET /api/memories/{memory_id}

If the AI module needs a new prediction/result endpoint, agree on the JSON contract with the backend developer before implementation.

Example conceptual result:

{

  "patient_id": 2,

  "prediction": "ATTENTION_REQUIRED",

  "confidence": 0.87

}

This is only an example contract. It is not an existing endpoint unless added to Swagger.

7. MEMBER 4 — Location & Safety

Send Patient Location

POST /api/location/

Auth: Patient

The backend associates the location with the authenticated patient.

Caregiver Latest Location

GET /api/location/caregiver/{patient_id}

Auth: Authorized caregiver

Caregiver Location History

Use the location-history endpoint currently shown in Swagger.

Auth: Authorized caregiver

Create Safe Zone

POST /api/safe-zones/

Get Safe Zones

GET /api/safe-zones/

Update Safe Zone

PUT /api/safe-zones/{safe_zone_id}

Delete Safe Zone

DELETE /api/safe-zones/{safe_zone_id}

SOS Emergency

POST /api/emergency/sos

Auth: Patient

When SOS is triggered:

an emergency event is stored

an SOS alert is created

caregiver in-app notification is generated

External push/SMS delivery is a separate notification integration.

8. MEMBER 6 — Caregiver Dashboard

Patient Overview

GET /api/caregiver/patients/{patient_id}/overview

Example response:

{

  "patient_id": 2,

  "name": "patient2",

  "age": 0,

  "language": "northeast",

  "orientation_status": "GOOD",

  "last_active": "2026-09-03T20:00:00+05:30",

  "overall_status": "ATTENTION",

  "alerts_count": 3,

  "medicine_adherence": 0,

  "missed_reminders": 4,

  "games_completed": 1,

  "average_game_accuracy": 85,

  "cognitive_trend": "INSUFFICIENT_DATA"

}

Use Swagger as the source of truth if fields change.

Patient Activity

GET /api/caregiver/patients/{patient_id}/activity

Provides caregiver-facing activity such as game completions, memory recall activity, voice-command activity, daily progress, and activity summary.

9. Alerts

Patient Alerts

GET /api/alerts/patient

Auth: Patient

Resolve Alert

PUT /api/alerts/{alert_id}/resolve

Caregiver Alerts

GET /api/alerts/caregiver/{patient_id}

Auth: Authorized caregiver

Automatic Missed Reminder Alert

When the backend detects at least 3 missed reminders in the configured 7-day period, it can create a MISSED_REMINDERS alert and a caregiver in-app notification.

Clients do not need to manually create this alert.

10. Notifications

Get Notifications

GET /api/notifications/

Auth: Current authenticated user

Get Unread Notifications

GET /api/notifications/unread

Get Unread Count

GET /api/notifications/unread-count

Mark Notification as Read

PUT /api/notifications/{notification_id}/read

Mark All as Read

PUT /api/notifications/read-all

Current notification types include:

SOS

SAFE_ZONE_EXIT

MISSED_REMINDERS

Notifications are currently stored as in-app database notifications. External FCM push delivery is a separate future integration.

11. Device Tokens

Register Device Token

POST /api/device-tokens/

Example:

{

  "token": "device-token-from-app",

  "platform": "android"

}

Supported platforms:

android

ios

web

Get Current User's Active Tokens

GET /api/device-tokens/

Deactivate Device Token

DELETE /api/device-tokens/{token_id}

12. Reminders

Create Reminder

POST /api/reminders/

Example:

{

  "medicine_id": 1,

  "voice_recording_id": 2,

  "reminder_type": "MEDICINE",

  "reminder_text": "Please take your medicine.",

  "scheduled_time": "14:30:00",

  "repeat_pattern": "DAILY"

}

A reminder can reference a voice recording.

Update Reminder

PUT /api/reminders/{reminder_id}

Get Reminders

GET /api/reminders/

Get One Reminder

GET /api/reminders/{reminder_id}

Delete Reminder

DELETE /api/reminders/{reminder_id}

Record Reminder Event

POST /api/reminders/event

Example:

{

  "reminder_id": 3,

  "status": "MISSED"

}

13. Offline Synchronization

Sync Offline Events

POST /api/sync/

Auth: Patient

Example:

{

  "patient_id": 2,

  "device_id": "test-device-001",

  "last_sync_at": "2026-09-04T09:01:03.380Z",

  "events": [

    {

      "event_id": "offline-test-001",

      "event_type": "REMINDER_MISSED",

      "data": {

        "reminder_id": 3,

        "status": "MISSED"

      },

      "timestamp": "2026-09-04T09:01:00+05:30"

    }

  ]

}

Response contains:

{

  "success": true,

  "synced_events": 1,

  "failed_events": [],

  "server_updates": {

    "reminders": [],

    "memories": [],

    "family": []

  },

  "next_sync_token": "server-generated-token"

}

The backend uses event_id + patient_id + device_id to prevent duplicate processing.

Server updates can contain current reminders, memories, and active family members.

14. Family Members

Useful endpoints:

POST /api/family-members/

GET  /api/family-members/

GET  /api/family-members/{family_member_id}

PUT  /api/family-members/{family_member_id}

DELETE /api/family-members/{family_member_id}

Use Swagger for the exact current schemas.

A family member can be marked as a caregiver.

15. Integration Rules

Rule 1 — Never access PostgreSQL directly

Correct:

Frontend / AI / Safety

        ↓

     FastAPI

        ↓

   PostgreSQL

Incorrect:

Frontend

   ↓

PostgreSQL

Rule 2 — Always use JWT

Authorization: Bearer <YOUR_TOKEN>

Rule 3 — Swagger is the source of truth

Local:

http://127.0.0.1:8000/docs

For team integration, replace the host with the shared/deployed backend URL.

Rule 4 — Backend handles ownership

Do not assume changing patient_id gives access to another patient. Backend authorization checks ownership and caregiver relationships.

Rule 5 — Each member integrates their own module

Member 1 → Memories/Voice → Backend

Member 2 → Games → Backend

Member 3 → AI → Backend

Member 4 → Safety → Backend

Member 6 → Caregiver Dashboard → Backend

The backend developer provides and maintains the API contract.

16. Quick API Map

Member  Main APIs

Member 1    Memories, Voice Recordings, Audio Upload

Member 2    Games, Game Sessions, Game Results

Member 3    Game Performance, Activity, Memory Data

Member 4    Location, Safe Zones, SOS

Member 5    Backend, Database, Authentication, APIs, Sync, Notifications

Member 6    Caregiver Overview, Activity, Alerts, Notifications, Performance, Location

17. Before Integration Checklist

Backend

Backend runs successfully

Swagger opens

requirements.txt is updated

.env is NOT committed

Secrets are NOT committed

API contract is shared

Shared/deployed base URL is provided

Other team members

Get the correct Base URL

Create/use their own test account

Obtain their own JWT

Add Authorization: Bearer <token>

Test the API in Swagger first

Connect their own module

Do not access PostgreSQL directly

Report missing API fields/endpoints to the backend developer

18. Current Limitations

Database/in-app notification functionality is available.

Actual Firebase/FCM push delivery can be added later.

Deployment can be completed after local integration is verified.

Final Integration Flow

                 MEMORA FASTAPI BACKEND

                         │

       ┌─────────────────┼─────────────────┐

       │                 │                 │

       ↓                 ↓                 ↓

   Patient App       AI Service      Caregiver Dashboard

       │                 │                 │

       ├─ Memories       ├─ Analysis       ├─ Overview

       ├─ Voice          ├─ Performance    ├─ Alerts

       ├─ Games          └─ Activity       ├─ Notifications

       ├─ Reminders                       ├─ Games

       ├─ Location                        └─ Location

       └─ SOS

                         │

                         ↓

                    PostgreSQL

Swagger is the final source of truth for exact schemas and endpoint details.