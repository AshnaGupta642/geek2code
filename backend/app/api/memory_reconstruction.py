import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.core.dependencies import get_current_user

from app.models.patient import Patient
from app.models.memory import Memory

from app.schemas.memory_reconstruction import (
    MemoryReconstructionStartRequest,
    MemoryReconstructionStartResponse,
    MemoryReconstructionAnswerRequest,
    MemoryReconstructionAnswerResponse
)

from app.services.memory_reconstruction_service import (
    MemoryReconstructionService
)


router = APIRouter(
    prefix="/api/memory-reconstruction",
    tags=["Memory Reconstruction"]
)

reconstruction_service = MemoryReconstructionService()


@router.post(
    "/start",
    response_model=MemoryReconstructionStartResponse
)
def start_reconstruction(
    request: MemoryReconstructionStartRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

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

    if patient.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized for this patient"
        )

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
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Memory not found"
        )

    session_id = str(uuid.uuid4())

    try:
        result = reconstruction_service.start_session(
            patient_id=patient.id,
            memory_id=memory.id,
            language=request.language
        )

        result["session_id"] = session_id

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


@router.post(
    "/answer",
    response_model=MemoryReconstructionAnswerResponse
)
def submit_answer(
    request: MemoryReconstructionAnswerRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

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

    if patient.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized for this patient"
        )

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
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Memory not found"
        )

    try:
        result = reconstruction_service.submit_answer(
            session_id=request.session_id,
            patient_id=patient.id,
            memory_id=memory.id,
            answer_text=request.answer_text
        )

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