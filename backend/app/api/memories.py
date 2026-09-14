# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session

# from app.database.database import get_db
# from app.models.memory import Memory
# from app.models.patient import Patient
# from app.models.user import User
# from app.schemas.memory import (
#     MemoryCreate,
#     MemoryUpdate,
#     MemoryResponse
# )
# from app.core.dependencies import get_current_user


# router = APIRouter(
#     prefix="/api/memories",
#     tags=["Memories"]
# )


# # =========================================================
# # CREATE MEMORY
# # =========================================================

# @router.post("/", response_model=MemoryResponse)
# def create_memory(
#     memory_data: MemoryCreate,
#     current_user: User = Depends(get_current_user),
#     db: Session = Depends(get_db)
# ):

#     patient = (
#         db.query(Patient)
#         .filter(Patient.user_id == current_user.id)
#         .first()
#     )

#     if not patient:
#         raise HTTPException(
#             status_code=404,
#             detail="Patient profile not found"
#         )

#     memory = Memory(
#         patient_id=patient.id,
#         title=memory_data.title,
#         story_text=memory_data.story_text,
#         summary=memory_data.summary,
#         memory_type=memory_data.memory_type,
#         tags=memory_data.tags,
#         people=memory_data.people,
#         event_date=memory_data.event_date,
#         location=memory_data.location,
#         cover_photo_url=memory_data.cover_photo_url,
#         audio_url=memory_data.audio_url,
#         is_private=memory_data.is_private,

#         # Approval should not be controlled directly by the patient
#         is_approved=False
#     )

#     db.add(memory)
#     db.commit()
#     db.refresh(memory)

#     return memory


# # =========================================================
# # GET ALL MEMORIES
# # =========================================================

# @router.get("/", response_model=list[MemoryResponse])
# def get_memories(
#     current_user: User = Depends(get_current_user),
#     db: Session = Depends(get_db)
# ):

#     patient = (
#         db.query(Patient)
#         .filter(Patient.user_id == current_user.id)
#         .first()
#     )

#     if not patient:
#         raise HTTPException(
#             status_code=404,
#             detail="Patient profile not found"
#         )

#     memories = (
#         db.query(Memory)
#         .filter(Memory.patient_id == patient.id)
#         .order_by(Memory.created_at.desc())
#         .all()
#     )

#     return memories


# # =========================================================
# # GET SINGLE MEMORY
# # =========================================================

# @router.get("/{memory_id}", response_model=MemoryResponse)
# def get_memory(
#     memory_id: int,
#     current_user: User = Depends(get_current_user),
#     db: Session = Depends(get_db)
# ):

#     patient = (
#         db.query(Patient)
#         .filter(Patient.user_id == current_user.id)
#         .first()
#     )

#     if not patient:
#         raise HTTPException(
#             status_code=404,
#             detail="Patient profile not found"
#         )

#     memory = (
#         db.query(Memory)
#         .filter(
#             Memory.id == memory_id,
#             Memory.patient_id == patient.id
#         )
#         .first()
#     )

#     if not memory:
#         raise HTTPException(
#             status_code=404,
#             detail="Memory not found"
#         )

#     return memory


# # =========================================================
# # UPDATE MEMORY
# # =========================================================

# @router.put("/{memory_id}", response_model=MemoryResponse)
# def update_memory(
#     memory_id: int,
#     memory_data: MemoryUpdate,
#     current_user: User = Depends(get_current_user),
#     db: Session = Depends(get_db)
# ):

#     patient = (
#         db.query(Patient)
#         .filter(Patient.user_id == current_user.id)
#         .first()
#     )

#     if not patient:
#         raise HTTPException(
#             status_code=404,
#             detail="Patient profile not found"
#         )

#     memory = (
#         db.query(Memory)
#         .filter(
#             Memory.id == memory_id,
#             Memory.patient_id == patient.id
#         )
#         .first()
#     )

#     if not memory:
#         raise HTTPException(
#             status_code=404,
#             detail="Memory not found"
#         )

#     # Update only fields actually provided in the request
#     update_data = memory_data.model_dump(exclude_unset=True)

#     # Patient cannot directly approve a memory
#     update_data.pop("is_approved", None)

#     for field, value in update_data.items():
#         setattr(memory, field, value)

#     db.commit()
#     db.refresh(memory)

#     return memory


# # =========================================================
# # DELETE MEMORY
# # =========================================================

# @router.delete("/{memory_id}")
# def delete_memory(
#     memory_id: int,
#     current_user: User = Depends(get_current_user),
#     db: Session = Depends(get_db)
# ):

#     patient = (
#         db.query(Patient)
#         .filter(Patient.user_id == current_user.id)
#         .first()
#     )

#     if not patient:
#         raise HTTPException(
#             status_code=404,
#             detail="Patient profile not found"
#         )

#     memory = (
#         db.query(Memory)
#         .filter(
#             Memory.id == memory_id,
#             Memory.patient_id == patient.id
#         )
#         .first()
#     )

#     if not memory:
#         raise HTTPException(
#             status_code=404,
#             detail="Memory not found"
#         )

#     db.delete(memory)
#     db.commit()

#     return {
#         "success": True,
#         "message": "Memory deleted successfully"
#     }

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.memory import Memory
from app.models.patient import Patient
from app.schemas.memory import (
    MemoryCreate,
    MemoryUpdate,
    MemoryResponse
)
from app.core.dependencies import get_authorized_patient


router = APIRouter(
    prefix="/api/memories",
    tags=["Memories"]
)


# =========================================================
# CREATE MEMORY
# =========================================================

@router.post("/", response_model=MemoryResponse)
def create_memory(
    memory_data: MemoryCreate,
    patient: Patient = Depends(get_authorized_patient),
    db: Session = Depends(get_db)
):

    memory = Memory(
        patient_id=patient.id,
        title=memory_data.title,
        story_text=memory_data.story_text,
        summary=memory_data.summary,
        memory_type=memory_data.memory_type,
        tags=memory_data.tags,
        people=memory_data.people,
        event_date=memory_data.event_date,
        location=memory_data.location,
        cover_photo_url=memory_data.cover_photo_url,
        audio_url=memory_data.audio_url,
        is_private=memory_data.is_private,

        # Approval should not be controlled directly by the patient
        is_approved=False
    )

    db.add(memory)
    db.commit()
    db.refresh(memory)

    return memory


# =========================================================
# GET ALL MEMORIES
# =========================================================

@router.get("/", response_model=list[MemoryResponse])
def get_memories(
    patient: Patient = Depends(get_authorized_patient),
    db: Session = Depends(get_db)
):

    memories = (
        db.query(Memory)
        .filter(Memory.patient_id == patient.id)
        .order_by(Memory.created_at.desc())
        .all()
    )

    return memories


# =========================================================
# GET SINGLE MEMORY
# =========================================================

@router.get("/{memory_id}", response_model=MemoryResponse)
def get_memory(
    memory_id: int,
    patient: Patient = Depends(get_authorized_patient),
    db: Session = Depends(get_db)
):

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
            detail="Memory not found"
        )

    return memory


# =========================================================
# UPDATE MEMORY
# =========================================================

@router.put("/{memory_id}", response_model=MemoryResponse)
def update_memory(
    memory_id: int,
    memory_data: MemoryUpdate,
    patient: Patient = Depends(get_authorized_patient),
    db: Session = Depends(get_db)
):

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
            detail="Memory not found"
        )

    # Update only fields actually provided in the request
    update_data = memory_data.model_dump(exclude_unset=True)

    # Patient cannot directly approve a memory
    update_data.pop("is_approved", None)

    for field, value in update_data.items():
        setattr(memory, field, value)

    db.commit()
    db.refresh(memory)

    return memory


# =========================================================
# DELETE MEMORY
# =========================================================

@router.delete("/{memory_id}")
def delete_memory(
    memory_id: int,
    patient: Patient = Depends(get_authorized_patient),
    db: Session = Depends(get_db)
):

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
            detail="Memory not found"
        )

    db.delete(memory)
    db.commit()

    return {
        "success": True,
        "message": "Memory deleted successfully"
    }