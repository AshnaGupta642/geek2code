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