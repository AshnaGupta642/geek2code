import logging
import os

import requests

logger = logging.getLogger(__name__)

AI_SERVICE_URL = os.getenv("AI_SERVICE_URL", "http://127.0.0.1:8001")
BACKEND_BASE_URL = os.getenv("BACKEND_BASE_URL", "http://127.0.0.1:8000")

# A full voice turn (download, transcribe, LLM, synthesize) can take a
# while, especially for regional languages bridging through Bhashini
# + translation + Gemini + translation + Bhashini again.
REQUEST_TIMEOUT_SECONDS = 120


class AIVoiceService:
    """Calls the ai-service's /ai-voice/process endpoint over HTTP."""

    def process_voice(
        self,
        patient_id: int,
        audio_url: str,
        language: str,
        conversation_id: str,
    ) -> dict:
        """
        Args:
            patient_id: Backend's integer patient ID.
            audio_url: URL or backend-relative path to the patient's
                audio (e.g. "/audio/file.wav" or "audio/file.wav").
            language: Language code.
            conversation_id: Conversation ID.

        Returns:
            dict matching AIVoiceResponse's fields.

        Raises:
            ValueError: If audio_url is empty.
            RuntimeError: If ai-service is unreachable, times out,
                or returns an error.
        """
        if not audio_url or not audio_url.strip():
            raise ValueError("audio_url cannot be empty.")

        resolved_audio_url = self._resolve_audio_url(audio_url)

        payload = {
            "patient_id": patient_id,
            "audio_url": resolved_audio_url,
            "language": language,
            "conversation_id": conversation_id,
        }

        logger.info(
            "Calling ai-service: patient_id=%s, conversation_id=%s, language=%s",
            patient_id,
            conversation_id,
            language,
        )

        try:
            response = requests.post(
                f"{AI_SERVICE_URL}/ai-voice/process",
                json=payload,
                timeout=REQUEST_TIMEOUT_SECONDS,
            )
            response.raise_for_status()

            result = response.json()

            response_audio_url = result.get("response_audio_url")

            if response_audio_url and not response_audio_url.startswith(("http://", "https://")):
                filename = os.path.basename(response_audio_url)
                result["response_audio_url"] = f"{AI_SERVICE_URL.rstrip('/')}/audio/{filename}"

            logger.info(
                "ai-service responded successfully for conversation_id=%s",
                conversation_id
            )

            return result
        except requests.exceptions.Timeout as exc:
            logger.error("ai-service request timed out: %s", exc)
            raise RuntimeError("AI service request timed out.") from exc

        except requests.exceptions.ConnectionError as exc:
            logger.error("Could not connect to ai-service at %s: %s", AI_SERVICE_URL, exc)
            raise RuntimeError("Could not connect to AI service.") from exc

        except requests.exceptions.HTTPError as exc:
            detail = str(exc)
            try:
                detail = exc.response.json().get("detail", detail)
            except (ValueError, AttributeError):
                pass
            logger.error("ai-service returned an error: %s", detail)
            raise RuntimeError(f"AI service returned an error: {detail}") from exc

        except requests.exceptions.RequestException as exc:
            logger.error("ai-service request failed: %s", exc)
            raise RuntimeError(f"AI service request failed: {exc}") from exc

    @staticmethod
    def _resolve_audio_url(audio_url: str) -> str:
        """
        Turn a backend-relative path (with or without a leading slash,
        e.g. "/audio/file.wav" or "audio/file.wav") into a full URL.
        Already-full URLs (http:// or https://) are returned unchanged.
        """
        if audio_url.startswith(("http://", "https://")):
            return audio_url
        return f"{BACKEND_BASE_URL.rstrip('/')}/{audio_url.lstrip('/')}"

