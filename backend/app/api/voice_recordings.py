from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.core.dependencies import get_current_user

from app.models.user import User
from app.models.patient import Patient
from app.models.family_member import FamilyMember
from app.models.memory import Memory
from app.models.voice_recording import VoiceRecording

from app.schemas.voice_recording import (
    VoiceRecordingCreate,
    VoiceRecordingResponse
)


router = APIRouter(
    prefix="/api/voice-recordings",
    tags=["Voice Recordings"]
)


# --------------------------------------------------
# CREATE VOICE RECORDING - PATIENT
# --------------------------------------------------

@router.post(
    "/",
    response_model=VoiceRecordingResponse
)
def create_voice_recording(
    recording_data: VoiceRecordingCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    # Find logged-in patient's profile
    patient = (
        db.query(Patient)
        .filter(Patient.user_id == current_user.id)
        .first()
    )

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient profile not found"
        )

    # Validate memory ownership if memory_id is provided
    if recording_data.memory_id is not None:

        memory = (
            db.query(Memory)
            .filter(
                Memory.id == recording_data.memory_id,
                Memory.patient_id == patient.id
            )
            .first()
        )

        if not memory:
            raise HTTPException(
                status_code=404,
                detail="Memory not found for this patient"
            )

    # Validate family member ownership if provided
    if recording_data.family_member_id is not None:

        family_member = (
            db.query(FamilyMember)
            .filter(
                FamilyMember.id == recording_data.family_member_id,
                FamilyMember.patient_id == patient.id,
                FamilyMember.is_active == True
            )
            .first()
        )

        if not family_member:
            raise HTTPException(
                status_code=404,
                detail="Family member not found for this patient"
            )

    recording = VoiceRecording(
        patient_id=patient.id,
        family_member_id=recording_data.family_member_id,
        memory_id=recording_data.memory_id,
        audio_url=recording_data.audio_url,
        language=recording_data.language,
        recording_type=recording_data.recording_type,
        duration_seconds=recording_data.duration_seconds
    )

    db.add(recording)
    db.commit()
    db.refresh(recording)

    return recording


# --------------------------------------------------
# GET PATIENT VOICE RECORDINGS
# --------------------------------------------------

@router.get(
    "/",
    response_model=list[VoiceRecordingResponse]
)
def get_voice_recordings(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    patient = (
        db.query(Patient)
        .filter(Patient.user_id == current_user.id)
        .first()
    )

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient profile not found"
        )

    recordings = (
        db.query(VoiceRecording)
        .filter(
            VoiceRecording.patient_id == patient.id
        )
        .order_by(VoiceRecording.created_at.desc())
        .all()
    )

    return recordings


# --------------------------------------------------
# GET SINGLE VOICE RECORDING
# --------------------------------------------------

@router.get(
    "/{recording_id}",
    response_model=VoiceRecordingResponse
)
def get_voice_recording(
    recording_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    patient = (
        db.query(Patient)
        .filter(Patient.user_id == current_user.id)
        .first()
    )

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient profile not found"
        )

    recording = (
        db.query(VoiceRecording)
        .filter(
            VoiceRecording.id == recording_id,
            VoiceRecording.patient_id == patient.id
        )
        .first()
    )

    if not recording:
        raise HTTPException(
            status_code=404,
            detail="Voice recording not found"
        )

    return recording


# --------------------------------------------------
# GET VOICE RECORDINGS - CAREGIVER
# --------------------------------------------------

@router.get(
    "/caregiver/{patient_id}",
    response_model=list[VoiceRecordingResponse]
)
def get_patient_voice_recordings_for_caregiver(
    patient_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    # Logged-in user must be caregiver
    if current_user.role != "caregiver":
        raise HTTPException(
            status_code=403,
            detail="Only caregivers can access patient voice recordings"
        )

    # Verify caregiver-patient relationship
    caregiver = (
        db.query(FamilyMember)
        .filter(
            FamilyMember.user_id == current_user.id,
            FamilyMember.patient_id == patient_id,
            FamilyMember.is_caregiver == True,
            FamilyMember.is_active == True
        )
        .first()
    )

    if not caregiver:
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to access this patient's recordings"
        )

    recordings = (
        db.query(VoiceRecording)
        .filter(
            VoiceRecording.patient_id == patient_id
        )
        .order_by(VoiceRecording.created_at.desc())
        .all()
    )

    return recordings