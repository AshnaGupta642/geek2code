from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.core.dependencies import get_current_user

from app.models.user import User
from app.models.patient import Patient
from app.models.memory import Memory

from app.schemas.memory import (
    PersonalMemoryVaultRequest,
    PersonalMemoryVaultResponse
)

from app.services.personal_memory_service import (
    PersonalMemoryService
)


router = APIRouter(
    prefix="/api/personal-memory",
    tags=["Personal Memory Vault"]
)


@router.post(
    "/process",
    response_model=PersonalMemoryVaultResponse
)
def process_personal_memory(
    request: PersonalMemoryVaultRequest,
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
            detail="You are not authorized for this patient."
        )

    # --------------------------------------------------
    # 2. Verify memory ownership
    # --------------------------------------------------

    memory = (
        db.query(Memory)
        .filter(
            Memory.id == request.memory_id,
            Memory.patient_id == patient.id
        )
        .first()
    )

    if not memory:
        raise HTTPException(
            status_code=404,
            detail="Memory not found."
        )

    # --------------------------------------------------
    # 3. Call AI service
    # --------------------------------------------------

    try:

        service = PersonalMemoryService()

        result = service.process_memory(
            patient_id=patient.id,
            memory_id=memory.id,
            title=request.title,
            story_text=request.story_text,
            voice_recording_url=request.voice_recording_url,
            photo_urls=request.photo_urls
        )

    except NotImplementedError:

        raise HTTPException(
            status_code=503,
            detail="Personal Memory AI service is not connected yet."
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Personal Memory processing failed: {str(e)}"
        )

    # --------------------------------------------------
    # 4. Return AI result
    # --------------------------------------------------

    return PersonalMemoryVaultResponse(
        memory_id=memory.id,
        people=result.get("people", []),
        places=result.get("places", []),
        events=result.get("events", []),
        dates=result.get("dates", []),
        objects=result.get("objects", []),
        emotions=result.get("emotions", []),
        summary=result.get("summary")
    )