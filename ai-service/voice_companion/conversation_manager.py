import logging
from pathlib import Path
from typing import Optional
from uuid import uuid4

import requests

from voice_companion.context_manager import ContextManager
from voice_companion.prompts import build_voice_companion_prompt
from language_engine.language_config import is_supported, get_unsupported_language_message
from language_engine.speech_language_router import SpeechLanguageRouter

logger = logging.getLogger(__name__)

DOWNLOAD_TIMEOUT_SECONDS = 15
AUDIO_OUTPUT_DIR = Path(__file__).parent.parent / "data" / "audio_responses"
AUDIO_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


class ConversationManager:
    """
    Connects Speech-to-Text, LLM, Text-to-Speech, and multi-turn
    conversation history for the AI Voice Companion — routed through
    SpeechLanguageRouter so each of the 7 supported languages goes
    through the correct provider (Gemini directly for en/hi/bn, or a
    Bhashini-based translate-bridge pipeline for as/ml/mni/brx).
    """

    def __init__(
        self,
        router: Optional[SpeechLanguageRouter] = None,
        context_manager: Optional[ContextManager] = None,
    ):
        self.router = router or SpeechLanguageRouter()
        self.context_manager = context_manager or ContextManager()

    def process_conversation(
        self,
        patient_id: str,
        audio_url: Optional[str] = None,
        language: str = "en",
        conversation_id: Optional[str] = None,
        extra_context: str = "",
        audio_path: Optional[str] = None,
    ) -> dict:
        """
        Process one complete patient voice interaction.

        Args:
            patient_id: Unique patient identifier.
            audio_url: Optional URL of the patient's audio. Kept for API/backend
                integrations where audio is uploaded and exposed over HTTP.
            audio_path: Optional local path to an audio file. Useful for local
                testing and development; the source file is never deleted.
            language: Language code — one of the 7 supported by
                language_engine/language_config.py.
            conversation_id: Existing conversation ID. A new one is
                generated if not provided. Reuse the same ID across
                turns of the same session so history is maintained.
            extra_context: Optional additional context (e.g. from the
                memory vault) to append alongside the conversation
                history already tracked by ContextManager.

        Returns:
            Dictionary matching the Person 5 Voice Companion API response.

        Raises:
            ValueError: If required fields are missing or language is
                not supported (message includes what languages ARE
                supported, via language_config.get_unsupported_language_message()).
            RuntimeError: If download, transcription, LLM, or TTS steps fail.
        """
        if not patient_id:
            raise ValueError("patient_id is required.")
        if not audio_url and not audio_path:
            raise ValueError("Either audio_url or audio_path is required.")
        if not language:
            raise ValueError("language is required.")
        if not is_supported(language):
            raise ValueError(get_unsupported_language_message(language))

        if not conversation_id:
            conversation_id = str(uuid4())

        logger.info(
            "Processing conversation: patient=%s, conversation=%s, language=%s",
            patient_id,
            conversation_id,
            language,
        )

        # --------------------------------------------------
        # STEP 1: Acquire audio
        # --------------------------------------------------
        # Local files are used directly and are NOT deleted after processing.
        # HTTP/HTTPS audio is downloaded to a temporary file and is deleted
        # after processing.
        source_is_temporary = False
        if audio_path:
            acquired_audio_path = self._resolve_local_audio(audio_path)
        else:
            acquired_audio_path = self._download_audio(audio_url)
            source_is_temporary = True

        try:
            # --------------------------------------------------
            # STEP 2: Transcribe (routed by provider — Gemini or
            # Bhashini-with-English-bridge, handled inside the router)
            # --------------------------------------------------
            turn = self.router.transcribe_turn(
                audio_path=str(acquired_audio_path),
                language=language,
            )
            transcript = turn["transcript"]

            if not transcript:
                raise RuntimeError("Speech-to-text returned an empty transcript.")

            logger.info("Transcript: %s", transcript)
            if turn["notes"]:
                for note in turn["notes"]:
                    logger.warning("Transcription note: %s", note)

            # --------------------------------------------------
            # STEP 3: Detect intent.
            # NOTE: intent keywords (prompts.py's word lists via
            # _detect_intent below) are English-only. For regional
            # languages this works out because turn["llm_input_text"]
            # is already the English-bridged translation — but for
            # Hindi/Bengali (Gemini languages, not bridged), intent
            # detection still runs on non-English text and may not
            # match these English keywords well. This is a known,
            # pre-existing limitation, not something introduced by
            # this change — a future improvement would be running
            # intent detection on an English translation for every
            # language, not just the bridged ones.
            # --------------------------------------------------
            intent_detection_text = turn["llm_input_text"]
            intent = self._detect_intent(intent_detection_text)
            logger.info("Detected intent: %s", intent)

            # --------------------------------------------------
            # STEP 4: Build conversation context BEFORE adding
            # this turn's message, so the LLM sees prior turns only.
            # --------------------------------------------------
            history_context = self.context_manager.get_context(conversation_id)

            combined_context = history_context
            if extra_context:
                combined_context = (
                    f"{history_context}\n\n{extra_context}".strip()
                    if history_context
                    else extra_context
                )

            # The system prompt is built assuming the LLM reasons in
            # English when bridged (turn["bridged_through_english"]),
            # or directly in `language` otherwise — build_voice_companion_prompt
            # is given the LLM's actual reasoning language accordingly.
            prompt_language = "en" if turn["bridged_through_english"] else language

            system_prompt = build_voice_companion_prompt(
                language=prompt_language,
                context=combined_context,
                intent=intent,
            )

            # --------------------------------------------------
            # STEP 5: Generate response + synthesize speech
            # (routed by provider, with response-language verification
            # or back-translation handled inside the router)
            # --------------------------------------------------
            audio_output_path = AUDIO_OUTPUT_DIR / f"{conversation_id}_response.wav"

            result = self.router.respond_and_synthesize(
                llm_input_text=turn["llm_input_text"],
                target_language=language,
                system_prompt=system_prompt,
                output_audio_path=str(audio_output_path),
                bridged_through_english=turn["bridged_through_english"],
            )

            response_text = result["response_text"]
            response_audio_path = result["response_audio_path"]

            logger.info("AI response: %s", response_text)
            if result["notes"]:
                for note in result["notes"]:
                    logger.warning("Response note: %s", note)

            # NOTE: response_audio_path is a LOCAL FILE PATH, not a hosted URL.
            # Person 1 (Flutter app) and Person 5 (backend) will need an actual
            # URL to fetch this audio over the network. Before this integrates
            # with the real API, this file needs to be uploaded to whatever
            # storage Person 5's backend provides (S3, GCS, backend-served
            # static path, etc.), and THAT url returned here instead.
            # Returning a local disk path as "audio_url" will break integration.

            # --------------------------------------------------
            # STEP 6: Record this turn in conversation history
            # (after a successful LLM call, so a failed turn
            # doesn't pollute history with a one-sided message)
            # --------------------------------------------------
            self.context_manager.add_message(conversation_id, "user", transcript)
            self.context_manager.add_message(conversation_id, "assistant", response_text)

            # --------------------------------------------------
            # STEP 7: Return API response
            # --------------------------------------------------
            return {
                "conversation_id": conversation_id,
                "transcript": transcript,
                "response_text": response_text,
                "response_audio_url": response_audio_path,  # TODO: replace with real hosted URL
                "detected_language": language,
                "intent": intent,
                "provider": turn["provider"],
                "bridged_through_english": turn["bridged_through_english"],
            }

        finally:
            if source_is_temporary:
                self._cleanup_file(acquired_audio_path)

    @staticmethod
    def _resolve_local_audio(audio_path: str) -> Path:
        """
        Resolve a local audio file without modifying or deleting it.

        Relative paths are resolved first from the current working directory,
        then from the project root. This makes tests such as
        `tests/live_recording.wav` work when launched from PyCharm.
        """
        raw_path = Path(audio_path.replace("file://", "")).expanduser()

        candidates = [
            raw_path,
            Path.cwd() / raw_path,
            Path(__file__).resolve().parent.parent / raw_path,
        ]

        for candidate in candidates:
            if candidate.exists() and candidate.is_file():
                if candidate.stat().st_size == 0:
                    raise RuntimeError(f"Local audio file is empty: {candidate}")
                logger.info("Using local audio file: %s", candidate.resolve())
                return candidate.resolve()

        raise RuntimeError(
            "Local audio file not found. Checked: "
            + ", ".join(str(p.resolve()) for p in candidates)
        )

    @staticmethod
    def _download_audio(audio_url: str) -> Path:
        """
        Download audio from an HTTP/HTTPS URL to a temporary file.

        This path is intended for backend/API integrations where audio is
        uploaded by a client and exposed through a reachable URL.
        """
        if not audio_url:
            raise ValueError("audio_url is required for remote audio.")

        if not audio_url.startswith(("http://", "https://")):
            raise RuntimeError(
                f"Invalid remote audio URL: {audio_url}. "
                "Use http:// or https://, or pass a local file through audio_path."
            )

        suffix = Path(audio_url.split("?")[0]).suffix or ".wav"
        temp_path = Path.cwd() / f"_tmp_download_{uuid4().hex}{suffix}"

        try:
            response = requests.get(audio_url, timeout=DOWNLOAD_TIMEOUT_SECONDS)
            response.raise_for_status()
            temp_path.write_bytes(response.content)
        except requests.RequestException as exc:
            temp_path.unlink(missing_ok=True)
            raise RuntimeError(f"Could not download audio from audio_url: {exc}") from exc

        if not temp_path.exists() or temp_path.stat().st_size == 0:
            temp_path.unlink(missing_ok=True)
            raise RuntimeError(f"Downloaded audio file is empty or missing: {audio_url}")

        return temp_path

    @staticmethod
    def _cleanup_file(path: Path) -> None:
        """Delete temporary audio file."""
        try:
            if path.exists():
                path.unlink()
        except OSError:
            logger.warning("Could not delete temporary file: %s", path)

    @staticmethod
    def _detect_intent(text: str) -> str:
        """
        Basic keyword-based intent detection, run on English text
        (see the note at the call site in process_conversation()).
        Intentionally simple for now — can be replaced with an
        AI-based intent classifier later.

        Returned values must match keys in prompts.INTENT_PROMPT_MAP
        so the detected intent actually selects the right prompt.
        """
        lowered = text.lower()

        if any(word in lowered for word in ["hello", "hi", "hey"]):
            return "greeting"
        if any(word in lowered for word in ["medicine", "tablet", "pill"]):
            return "medicine"
        if any(word in lowered for word in ["sad", "lonely", "scared", "afraid"]):
            return "emotional_support"
        if any(word in lowered for word in ["where am i", "where is", "lost"]):
            return "orientation"
        if any(word in lowered for word in ["family", "mother", "father", "brother", "sister"]):
            return "family"

        return "general_conversation"


# ----------------------------------------------------------
# Simple local test
# ----------------------------------------------------------
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    manager = ConversationManager()

    try:
        result = manager.process_conversation(
            patient_id="P001",
            audio_path="tests/live_recording.wav",
            language="en",
            conversation_id="C001",
        )

        print("\nConversation Result:")
        print(result)

    except (ValueError, RuntimeError) as err:
        print(f"Error: {err}")