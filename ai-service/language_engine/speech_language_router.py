"""
Speech Language Router

The orchestration layer that ties language_config.py, translator.py,
response_localizer.py, and voice_companion/'s Gemini-based
speech_to_text.py / llm_client.py / text_to_speech.py together into
one routed pipeline, based on which provider handles which language.

Design rationale — why a translate-bridge, not just "call Bhashini
instead of Gemini":
Bhashini provides ASR, translation, and TTS — it does NOT provide a
conversational LLM. The actual "understanding what the patient said and
generating a warm, dementia-appropriate reply" step has to go through
Gemini regardless of language. But we've already established Gemini's
own understanding of some regional languages (Bodo especially) is weak
or unconfirmed. So for regional languages, the most reliable pipeline
is:

    1. Transcribe the patient's audio in their own language (Bhashini
       ASR — see NOTE below on current status)
    2. Translate that transcript to English (translator.py — real,
       working, via Bhashini)
    3. Let Gemini understand and respond in English, where it's
       strongest (llm_client.py — unchanged, reliable)
    4. Translate the English response back to the patient's language
       (translator.py again)
    5. Speak it in their language (Bhashini TTS — see NOTE below)

For Gemini-handled languages (en, hi, bn), none of this bridging is
needed — speech_to_text.py, llm_client.py, and text_to_speech.py are
called directly, exactly as conversation_manager.py already does today.

NOTE — current status of Bhashini ASR/TTS:
translator.py's Bhashini translation is confirmed working end-to-end
against a live account. Bhashini's text-language-detection task
(used by language_detector.py) has an UNCONFIRMED taskType string —
several guesses were rejected by the API, and it wasn't worth chasing
further since language detection isn't in this app's critical path
(the app always has the language pre-selected).

BhashiniASRClient and BhashiniTTSClient below ARE implemented, based
on Bhashini's officially documented request/response shapes for the
"asr" and "tts" taskTypes (confirmed via their public docs — not
guessed blindly, unlike the language-detection taskType). However,
unlike translator.py, these have NOT yet been tested against a live
account with real audio — test with a real audio file before trusting
this in a live conversation. If something fails, the same class of
bug we hit with translator.py (DHRUVA-101 from a stripped-down
"language" config missing script codes) is the first thing to check —
both classes already reuse the full config object to avoid that,
but TTS's optional fields (e.g. "gender") are less certain than ASR's.
Until proven, this router falls back to Gemini's own STT/TTS for
regional languages if Bhashini fails, clearly logged as a
lower-confidence path, rather than blocking the conversation entirely.
"""

import base64
import logging
import os
from typing import Dict, Optional

import requests

from .language_config import (
    PROVIDER_GEMINI,
    PROVIDER_REGIONAL_API,
    get_provider,
    is_supported,
)
from .response_localizer import ResponseLocalizer
from .translator import Translator

logger = logging.getLogger(__name__)

# Bridge language used for LLM reasoning when the patient's language
# isn't one Gemini handles reliably. English chosen since it's Gemini's
# strongest language and translator.py already bridges to/from it well.
BRIDGE_LANGUAGE = "en"


class BhashiniASRClient:
    """
    Real client for Bhashini's audio transcription (ASR) service.

    Based on Bhashini's official documented request/response shapes
    (confirmed via their public API docs), NOT guessed blindly:

    Request config needs "language", "serviceId", "audioFormat", and
    "samplingRate" as siblings inside the task's config object. Audio
    is sent base64-encoded under inputData.audio[0].audioContent, with
    inputData.input[0].source left as null (ASR doesn't take text input).

    Response shape: pipelineResponse[0].output[0].source holds the
    transcribed text.

    Same lesson from translator.py's DHRUVA-101 bug applies here: the
    "language" object from the pipeline config step is reused as-is
    (it may include a sourceScriptCode) rather than manually rebuilt.
    """

    ULCA_AUTH_URL = "https://meity-auth.ulcacontrib.org/ulca/apis/v0/model/getModelsPipeline"
    PIPELINE_ID = "64392f96daac500b55c543cd"
    REQUEST_TIMEOUT_SECONDS = 60
    INFERENCE_TIMEOUT_SECONDS = 60

    def __init__(self, user_id: Optional[str] = None, api_key: Optional[str] = None) -> None:
        self.user_id = user_id or os.getenv("BHASHINI_USER_ID")
        self.api_key = api_key or os.getenv("BHASHINI_API_KEY")
        self._pipeline_cache: Dict[str, Dict] = {}

    def is_configured(self) -> bool:
        return bool(self.user_id and self.api_key)

    def _get_pipeline_config(self, source_language: str) -> Dict:
        if source_language in self._pipeline_cache:
            return self._pipeline_cache[source_language]

        payload = {
            "pipelineTasks": [
                {"taskType": "asr", "config": {"language": {"sourceLanguage": source_language}}}
            ],
            "pipelineRequestConfig": {"pipelineId": self.PIPELINE_ID},
        }
        headers = {
            "userID": self.user_id,
            "ulcaApiKey": self.api_key,
            "Content-Type": "application/json",
        }

        response = requests.post(
            self.ULCA_AUTH_URL, json=payload, headers=headers, timeout=self.REQUEST_TIMEOUT_SECONDS
        )
        try:
            response.raise_for_status()
        except requests.HTTPError as exc:
            raise RuntimeError(
                f"Bhashini ASR pipeline config failed ({response.status_code}): {response.text}"
            ) from exc

        data = response.json()
        try:
            config_entry = data["pipelineResponseConfig"][0]["config"][0]
            inference_key_info = data["pipelineInferenceAPIEndPoint"]["inferenceApiKey"]
            config = {
                "language": config_entry["language"],
                "service_id": config_entry["serviceId"],
                "inference_api_key_name": inference_key_info["name"],
                "inference_api_key_value": inference_key_info["value"],
                "callback_url": data["pipelineInferenceAPIEndPoint"]["callbackUrl"],
            }
        except (KeyError, IndexError, TypeError) as exc:
            raise RuntimeError(f"Unexpected ASR pipeline config response shape: {data}") from exc

        self._pipeline_cache[source_language] = config
        return config

    def transcribe(
        self,
        audio_path: str,
        language: str,
        audio_format: str = "wav",
        sampling_rate: int = 16000,
    ) -> str:
        """
        Transcribe an audio file via Bhashini ASR.

        Raises:
            RuntimeError: If credentials are missing, config fetch fails,
                the audio file can't be read, or inference fails.
        """
        if not self.is_configured():
            raise RuntimeError(
                "Bhashini credentials are not configured "
                "(set BHASHINI_USER_ID and BHASHINI_API_KEY in .env)."
            )

        try:
            with open(audio_path, "rb") as audio_file:
                audio_base64 = base64.b64encode(audio_file.read()).decode("utf-8")
        except OSError as exc:
            raise RuntimeError(f"Could not read audio file '{audio_path}': {exc}") from exc

        config = self._get_pipeline_config(language)

        payload = {
            "pipelineTasks": [
                {
                    "taskType": "asr",
                    "config": {
                        "language": config["language"],
                        "serviceId": config["service_id"],
                        "audioFormat": audio_format,
                        "samplingRate": sampling_rate,
                    },
                }
            ],
            "inputData": {
                # Bhashini's own docs example shows "source": null here,
                # but live validation rejects None with a 422 error
                # ("none is not an allowed value") — use an empty string
                # instead, which their docs example apparently doesn't
                # reflect accurately.
                "input": [{"source": ""}],
                "audio": [{"audioContent": audio_base64}],
            },
        }
        headers = {
            "Content-Type": "application/json",
            config["inference_api_key_name"]: config["inference_api_key_value"],
        }

        try:
            response = requests.post(
                config["callback_url"],
                json=payload,
                headers=headers,
                timeout=self.INFERENCE_TIMEOUT_SECONDS,
            )
        except requests.Timeout as exc:
            raise RuntimeError(f"Bhashini ASR inference call timed out: {exc}") from exc

        try:
            response.raise_for_status()
        except requests.HTTPError as exc:
            raise RuntimeError(
                f"Bhashini ASR inference failed ({response.status_code}): {response.text}"
            ) from exc

        data = response.json()
        try:
            return data["pipelineResponse"][0]["output"][0]["source"]
        except (KeyError, IndexError, TypeError) as exc:
            raise RuntimeError(f"Unexpected ASR inference response shape: {data}") from exc


class BhashiniTTSClient:
    """
    Real client for Bhashini's text-to-speech (TTS) service.

    Response contains base64-encoded audio at
    pipelineResponse[0].audio[0].audioContent, which is decoded and
    written to output_path (WAV format is Bhashini's typical default).

    NOTE: unlike ASR's documented shape, TTS's exact optional config
    fields (gender, sampling rate) weren't independently confirmed
    against live docs the way ASR's were — "gender" is included based
    on common usage seen across multiple third-party Bhashini
    integrations, but if this fails, check the actual pipeline config
    response for this language for any additional required fields.
    """

    ULCA_AUTH_URL = "https://meity-auth.ulcacontrib.org/ulca/apis/v0/model/getModelsPipeline"
    PIPELINE_ID = "64392f96daac500b55c543cd"
    REQUEST_TIMEOUT_SECONDS = 60
    INFERENCE_TIMEOUT_SECONDS = 60

    def __init__(self, user_id: Optional[str] = None, api_key: Optional[str] = None) -> None:
        self.user_id = user_id or os.getenv("BHASHINI_USER_ID")
        self.api_key = api_key or os.getenv("BHASHINI_API_KEY")
        self._pipeline_cache: Dict[str, Dict] = {}

    def is_configured(self) -> bool:
        return bool(self.user_id and self.api_key)

    def _get_pipeline_config(self, source_language: str) -> Dict:
        if source_language in self._pipeline_cache:
            return self._pipeline_cache[source_language]

        payload = {
            "pipelineTasks": [
                {"taskType": "tts", "config": {"language": {"sourceLanguage": source_language}}}
            ],
            "pipelineRequestConfig": {"pipelineId": self.PIPELINE_ID},
        }
        headers = {
            "userID": self.user_id,
            "ulcaApiKey": self.api_key,
            "Content-Type": "application/json",
        }

        response = requests.post(
            self.ULCA_AUTH_URL, json=payload, headers=headers, timeout=self.REQUEST_TIMEOUT_SECONDS
        )
        try:
            response.raise_for_status()
        except requests.HTTPError as exc:
            raise RuntimeError(
                f"Bhashini TTS pipeline config failed ({response.status_code}): {response.text}"
            ) from exc

        data = response.json()
        try:
            config_entry = data["pipelineResponseConfig"][0]["config"][0]
            inference_key_info = data["pipelineInferenceAPIEndPoint"]["inferenceApiKey"]
            config = {
                "language": config_entry["language"],
                "service_id": config_entry["serviceId"],
                "inference_api_key_name": inference_key_info["name"],
                "inference_api_key_value": inference_key_info["value"],
                "callback_url": data["pipelineInferenceAPIEndPoint"]["callbackUrl"],
            }
        except (KeyError, IndexError, TypeError) as exc:
            raise RuntimeError(f"Unexpected TTS pipeline config response shape: {data}") from exc

        self._pipeline_cache[source_language] = config
        return config

    def synthesize(
        self, text: str, language: str, output_path: str, gender: str = "female"
    ) -> str:
        """
        Synthesize speech via Bhashini TTS and save it to output_path.

        Raises:
            RuntimeError: If credentials are missing, config fetch fails,
                or inference fails.
        """
        if not self.is_configured():
            raise RuntimeError(
                "Bhashini credentials are not configured "
                "(set BHASHINI_USER_ID and BHASHINI_API_KEY in .env)."
            )

        config = self._get_pipeline_config(language)

        payload = {
            "pipelineTasks": [
                {
                    "taskType": "tts",
                    "config": {
                        "language": config["language"],
                        "serviceId": config["service_id"],
                        "gender": gender,
                    },
                }
            ],
            "inputData": {"input": [{"source": text}]},
        }
        headers = {
            "Content-Type": "application/json",
            config["inference_api_key_name"]: config["inference_api_key_value"],
        }

        try:
            response = requests.post(
                config["callback_url"],
                json=payload,
                headers=headers,
                timeout=self.INFERENCE_TIMEOUT_SECONDS,
            )
        except requests.Timeout as exc:
            raise RuntimeError(f"Bhashini TTS inference call timed out: {exc}") from exc

        try:
            response.raise_for_status()
        except requests.HTTPError as exc:
            raise RuntimeError(
                f"Bhashini TTS inference failed ({response.status_code}): {response.text}"
            ) from exc

        data = response.json()
        try:
            audio_base64 = data["pipelineResponse"][0]["audio"][0]["audioContent"]
        except (KeyError, IndexError, TypeError) as exc:
            raise RuntimeError(f"Unexpected TTS inference response shape: {data}") from exc

        audio_bytes = base64.b64decode(audio_base64)
        with open(output_path, "wb") as audio_file:
            audio_file.write(audio_bytes)

        return output_path


class SpeechLanguageRouter:
    """
    Routes a full voice turn (audio in -> transcript -> LLM response ->
    audio out) through the correct provider pipeline based on language.
    """

    def __init__(
        self,
        stt=None,
        llm=None,
        tts=None,
        translator: Optional[Translator] = None,
        response_localizer: Optional[ResponseLocalizer] = None,
        bhashini_asr: Optional[BhashiniASRClient] = None,
        bhashini_tts: Optional[BhashiniTTSClient] = None,
    ) -> None:
        # Imported lazily inside __init__ (rather than at module level)
        # so this file doesn't hard-fail to import if voice_companion
        # isn't on the path yet in some contexts (e.g. isolated testing
        # of language_engine/ alone).
        if stt is None or llm is None or tts is None:
            from voice_companion.speech_to_text import SpeechToText
            from voice_companion.llm_client import LLMClient
            from voice_companion.text_to_speech import TextToSpeech

            stt = stt or SpeechToText()
            llm = llm or LLMClient()
            tts = tts or TextToSpeech()

        self.stt = stt
        self.llm = llm
        self.tts = tts
        self.translator = translator or Translator()
        self.response_localizer = response_localizer or ResponseLocalizer(
            translator=self.translator
        )
        self.bhashini_asr = bhashini_asr or BhashiniASRClient()
        self.bhashini_tts = bhashini_tts or BhashiniTTSClient()

    # ---------------------------------------------------------
    # Main entry point
    # ---------------------------------------------------------

    def process_voice_turn(
        self,
        audio_path: str,
        language: str,
        system_prompt: Optional[str] = None,
        output_audio_path: Optional[str] = None,
    ) -> Dict[str, object]:
        """
        Convenience wrapper: run transcribe_turn() then
        respond_and_synthesize() back to back, for simple cases that
        don't need anything (like intent detection) done in between.

        Callers that need to inspect/use the transcript before deciding
        on a system_prompt (e.g. conversation_manager.py picking a
        prompt based on detected intent) should call transcribe_turn()
        and respond_and_synthesize() separately instead of this method.

        Args, Returns, Raises: see transcribe_turn() and
        respond_and_synthesize() — this method combines both.
        """
        turn = self.transcribe_turn(audio_path, language)

        result = self.respond_and_synthesize(
            llm_input_text=turn["llm_input_text"],
            target_language=language,
            system_prompt=system_prompt,
            output_audio_path=output_audio_path,
            bridged_through_english=turn["bridged_through_english"],
        )

        return {
            "transcript": turn["transcript"],
            "response_text": result["response_text"],
            "response_audio_path": result["response_audio_path"],
            "provider": turn["provider"],
            "bridged_through_english": turn["bridged_through_english"],
            "notes": turn["notes"] + result["notes"],
        }

    # ---------------------------------------------------------
    # Phase 1: transcription (routed by provider)
    # ---------------------------------------------------------

    def transcribe_turn(self, audio_path: str, language: str) -> Dict[str, object]:
        """
        Transcribe the patient's audio, routed by provider.

        Args:
            audio_path: Path to the patient's audio.
            language: One of the 7 supported language codes.

        Returns:
            {
                "transcript": str,          # in the patient's own language
                "llm_input_text": str,      # text to feed the LLM — same
                                             # as transcript for Gemini
                                             # languages; English-translated
                                             # for regional languages (bridge)
                "provider": "GEMINI" | "REGIONAL_API",
                "bridged_through_english": bool,
                "notes": list[str],
            }

        Raises:
            ValueError: If language is not supported.
            RuntimeError: If transcription fails with no viable fallback.
        """
        if not is_supported(language):
            raise ValueError(f"Language '{language}' is not supported.")

        provider = get_provider(language)
        notes: list = []

        if provider == PROVIDER_GEMINI:
            transcript = self.stt.transcribe(audio_path=audio_path, language=language)
            return {
                "transcript": transcript,
                "llm_input_text": transcript,
                "provider": provider,
                "bridged_through_english": False,
                "notes": notes,
            }

        # Regional language: transcribe in-language, then bridge to English
        transcript = self._transcribe(audio_path, language, notes)

        to_bridge = self.translator.translate(
            text=transcript, source_language=language, target_language=BRIDGE_LANGUAGE
        )
        if to_bridge["confidence"] == "low":
            notes.append("Transcript-to-English translation used a lower-confidence path.")

        return {
            "transcript": transcript,
            "llm_input_text": to_bridge["translated_text"],
            "provider": provider,
            "bridged_through_english": True,
            "notes": notes,
        }

    # ---------------------------------------------------------
    # Phase 2: LLM response + speech synthesis (routed by provider)
    # ---------------------------------------------------------

    def respond_and_synthesize(
        self,
        llm_input_text: str,
        target_language: str,
        system_prompt: Optional[str] = None,
        output_audio_path: Optional[str] = None,
        bridged_through_english: bool = False,
    ) -> Dict[str, object]:
        """
        Generate an LLM response and speak it, routed by provider.

        Args:
            llm_input_text: Text to feed the LLM — typically
                transcribe_turn()'s "llm_input_text" value.
            target_language: Language the spoken response should end up in.
            system_prompt: System prompt for the LLM call. If
                bridged_through_english is True, this should be written
                assuming the LLM is reasoning in English.
            output_audio_path: Optional path to save the response audio.
            bridged_through_english: Pass transcribe_turn()'s
                "bridged_through_english" value here, so the response
                gets translated back to target_language before speaking.

        Returns:
            {
                "response_text": str,        # in target_language
                "response_audio_path": str,
                "notes": list[str],
            }

        Raises:
            ValueError: If target_language is not supported.
            RuntimeError: If LLM generation or synthesis fails.
        """
        if not is_supported(target_language):
            raise ValueError(f"Language '{target_language}' is not supported.")

        notes: list = []

        response = self.llm.generate_response(
            user_text=llm_input_text, system_prompt=system_prompt
        )

        if bridged_through_english and target_language != BRIDGE_LANGUAGE:
            back_translation = self.translator.translate(
                text=response, source_language=BRIDGE_LANGUAGE, target_language=target_language
            )
            if back_translation["confidence"] == "low":
                notes.append(
                    "Response translation back to the target language was lower-confidence."
                )
            response_text = back_translation["translated_text"]
        else:
            localized = self.response_localizer.localize(response, target_language=target_language)
            response_text = localized["text"]
            if localized["was_corrected"]:
                notes.append(
                    f"Response was auto-corrected from {localized['detected_language']} "
                    f"to {target_language} before speaking."
                )

        provider = get_provider(target_language)
        if provider == PROVIDER_GEMINI:
            response_audio_path = self.tts.synthesize(
                text=response_text, output_path=output_audio_path
            )
        else:
            response_audio_path = self._synthesize(
                response_text, target_language, output_audio_path, notes
            )

        return {
            "response_text": response_text,
            "response_audio_path": response_audio_path,
            "notes": notes,
        }

    # ---------------------------------------------------------
    # ASR/TTS helpers with Bhashini-first, Gemini-fallback behavior
    # ---------------------------------------------------------

    def _transcribe(self, audio_path: str, language: str, notes: list) -> str:
        """Transcribe audio, preferring Bhashini ASR when available."""
        if self.bhashini_asr.is_configured():
            try:
                return self.bhashini_asr.transcribe(audio_path, language)
            except Exception as exc:
                logger.warning(
                    "Bhashini ASR failed (%s) for language=%s; falling back to Gemini STT. "
                    "Gemini's transcription quality for this language is unconfirmed.",
                    exc,
                    language,
                )
                notes.append(
                    f"Bhashini ASR unavailable/failed for {language}; used Gemini STT as fallback."
                )
        else:
            logger.info(
                "Bhashini ASR not configured; using Gemini STT for language=%s "
                "(quality for this language is unconfirmed).",
                language,
            )
            notes.append(f"Bhashini ASR not configured; used Gemini STT for {language}.")

        return self.stt.transcribe(audio_path=audio_path, language=language)

    def _synthesize(
        self, text: str, language: str, output_path: Optional[str], notes: list
    ) -> str:
        """Synthesize speech, preferring Bhashini TTS when available."""
        if self.bhashini_tts.is_configured():
            try:
                return self.bhashini_tts.synthesize(text, language, output_path)
            except Exception as exc:
                logger.warning(
                    "Bhashini TTS failed (%s) for language=%s; falling back to Gemini TTS. "
                    "Gemini's speech synthesis quality for this language is unconfirmed.",
                    exc,
                    language,
                )
                notes.append(
                    f"Bhashini TTS unavailable/failed for {language}; used Gemini TTS as fallback."
                )
        else:
            logger.info(
                "Bhashini TTS not configured; using Gemini TTS for language=%s "
                "(quality for this language is unconfirmed).",
                language,
            )
            notes.append(f"Bhashini TTS not configured; used Gemini TTS for {language}.")

        return self.tts.synthesize(text=text, output_path=output_path)


# ---------------------------------------------------------
# Simple test
# ---------------------------------------------------------

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    router = SpeechLanguageRouter()

    # This test requires a real audio file — adjust the path below.
    # For a Gemini-handled language (en/hi/bn), it runs the direct path.
    # For a regional language (as/ml/mni/brx), it runs the bridge path,
    # and will log fallback notes since Bhashini ASR/TTS aren't
    # implemented yet unless you've built and passed in your own clients.
    result = router.process_voice_turn(
        audio_path="sample_audio.wav",
        language="hi",
        system_prompt="You are a friendly voice companion. Respond in Hindi in one short sentence.",
    )

    print("\nResult:")
    for key, value in result.items():
        print(f"{key}: {value}")