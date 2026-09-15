import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.core.dependencies import get_current_user

from app.models.user import User
from app.models.patient import Patient

from app.schemas.ai_voice import (
    AIVoiceRequest,
    AIVoiceResponse
)

from app.services.ai_voice_service import AIVoiceService


router = APIRouter(
    prefix="/api/ai-voice",
    tags=["AI Voice"]
)


@router.post(
    "/process",
    response_model=AIVoiceResponse
)
def process_ai_voice(
    request: AIVoiceRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    # --------------------------------------------------
    # 1. Verify patient ownership
    # --------------------------------------------------

    patient = (
        db.query(Patient)
        .filter(
            Patient.id == request.patient_id,
            Patient.user_id == current_user.id
        )
        .first()
    )

    if not patient:
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to use AI Voice for this patient."
        )

    # --------------------------------------------------
    # 2. Conversation ID
    # --------------------------------------------------

    conversation_id = (
        request.conversation_id
        if request.conversation_id
        else str(uuid.uuid4())
    )

    # --------------------------------------------------
    # 3. Call AI Voice service
    # --------------------------------------------------

    try:

        ai_service = AIVoiceService()

        result = ai_service.process_voice(
            patient_id=patient.id,
            audio_url=request.audio_url,
            language=request.language,
            conversation_id=conversation_id
        )

    except NotImplementedError:

        raise HTTPException(
            status_code=503,
            detail="AI Voice service is not connected yet."
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"AI Voice processing failed: {str(e)}"
        )

    # --------------------------------------------------
    # 4. Return standardized response
    # --------------------------------------------------

    return AIVoiceResponse(
        conversation_id=result.get(
            "conversation_id",
            conversation_id
        ),
        transcript=result.get("transcript"),
        response_text=result.get("response_text"),
        response_audio_url=result.get("response_audio_url"),
        detected_language=result.get(
            "detected_language",
            request.language
        ),
        intent=result.get("intent")
    )