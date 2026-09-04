import os
import uuid

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.patient import Patient
from app.models.voice_recording import VoiceRecording
from app.models.memory import Memory
from app.models.family_member import FamilyMember
from app.core.dependencies import get_current_user


router = APIRouter(
    prefix="/api/audio",
    tags=["Audio Upload"]
)


UPLOAD_DIR = "uploads/audio"


ALLOWED_AUDIO_TYPES = {
    "audio/mpeg": ".mp3",
    "audio/wav": ".wav",
    "audio/x-wav": ".wav",
    "audio/mp4": ".m4a",
    "audio/x-m4a": ".m4a",
    "audio/ogg": ".ogg",
}


MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


@router.post("/upload")
async def upload_audio(
    file: UploadFile = File(...),

    memory_id: int | None = None,
    family_member_id: int | None = None,
    language: str = "en",
    recording_type: str = "VOICE_RECORDING",
    duration_seconds: int | None = None,

    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    # --------------------------------
    # 1. Check file type
    # --------------------------------
    if file.content_type not in ALLOWED_AUDIO_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Unsupported audio format. Allowed: MP3, WAV, M4A, OGG."
        )


    # --------------------------------
    # 2. Find logged-in patient
    # --------------------------------
    patient = (
        db.query(Patient)
        .filter(Patient.user_id == current_user.id)
        .first()
    )

    if not patient:
        raise HTTPException(
            status_code=403,
            detail="Only patients can upload audio."
        )


    # --------------------------------
    # 3. Validate memory
    # --------------------------------
    if memory_id is not None:

        memory = (
            db.query(Memory)
            .filter(
                Memory.id == memory_id,
                Memory.patient_id == patient.id
            )
            .first()
        )

        if not memory:
            raise HTTPException(
                status_code=404,
                detail="Memory not found for this patient."
            )


    # --------------------------------
    # 4. Validate family member
    # --------------------------------
    if family_member_id is not None:

        family_member = (
            db.query(FamilyMember)
            .filter(
                FamilyMember.id == family_member_id,
                FamilyMember.patient_id == patient.id,
                FamilyMember.is_active == True
            )
            .first()
        )

        if not family_member:
            raise HTTPException(
                status_code=404,
                detail="Family member not found for this patient."
            )


    # --------------------------------
    # 5. Validate duration
    # --------------------------------
    if duration_seconds is not None and duration_seconds < 0:
        raise HTTPException(
            status_code=400,
            detail="Duration cannot be negative."
        )


    # --------------------------------
    # 6. Read audio file
    # --------------------------------
    contents = await file.read()


    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="Audio file is too large. Maximum size is 10 MB."
        )


    # --------------------------------
    # 7. Create upload directory
    # --------------------------------
    os.makedirs(
        UPLOAD_DIR,
        exist_ok=True
    )


    # --------------------------------
    # 8. Generate unique filename
    # --------------------------------
    extension = ALLOWED_AUDIO_TYPES[file.content_type]

    filename = f"{uuid.uuid4()}{extension}"


    file_path = os.path.join(
        UPLOAD_DIR,
        filename
    )


    # --------------------------------
    # 9. Save audio file
    # --------------------------------
    with open(file_path, "wb") as audio_file:
        audio_file.write(contents)


    # URL accessible by frontend
    audio_url = f"/audio/{filename}"


    # --------------------------------
    # 10. Create VoiceRecording
    # --------------------------------
    recording = VoiceRecording(
        patient_id=patient.id,
        memory_id=memory_id,
        family_member_id=family_member_id,
        audio_url=audio_url,
        language=language,
        recording_type=recording_type,
        duration_seconds=duration_seconds
    )


    db.add(recording)

    db.commit()

    db.refresh(recording)


    # --------------------------------
    # 11. Return response
    # --------------------------------
    return {
        "message": "Audio uploaded successfully",

        "recording_id": recording.id,

        "patient_id": patient.id,

        "memory_id": recording.memory_id,

        "family_member_id": recording.family_member_id,

        "filename": filename,

        "audio_url": audio_url,

        "language": recording.language,

        "recording_type": recording.recording_type,

        "duration_seconds": recording.duration_seconds,

        "content_type": file.content_type,

        "size_bytes": len(contents)
    }