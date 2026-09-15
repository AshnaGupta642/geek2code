from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.core.dependencies import get_current_user

from app.models.patient import Patient
from app.models.memory import Memory

from app.schemas.memory_graph import (
    MemoryGraphRequest,
    MemoryGraphResponse
)

from app.services.memory_graph_service import MemoryGraphService


router = APIRouter(
    prefix="/api/memory-graph",
    tags=["Memory Graph"]
)

memory_graph_service = MemoryGraphService()


@router.post(
    "/generate",
    response_model=MemoryGraphResponse
)
def generate_memory_graph(
    request: MemoryGraphRequest,
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
        result = memory_graph_service.generate_graph(
            memory_id=memory.id,
            patient_id=patient.id,
            people=request.people,
            places=request.places,
            events=request.events,
            photo_ids=request.photo_ids
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