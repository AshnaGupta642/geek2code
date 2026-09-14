from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.patient import Patient
from app.models.user import User
from app.core.dependencies import get_current_user
from app.schemas.patient import (
    PatientProfileCreate,
    PatientProfileResponse,
    PatientProfileUpdate
)

router = APIRouter(
    prefix="/api/patients",
    tags=["Patients"]
)

patient_router = APIRouter(
    prefix="/api/patient",
    tags=["Patient"]
)


def first_name_from_full_name(full_name: str | None) -> str:
    parts = (full_name or "").strip().split()
    return parts[0] if parts else ""


def serialize_patient_profile(patient: Patient, user: User | None) -> dict:
    name = (user.name if user else "") or ""
    return {
        "id": patient.id,
        "user_id": patient.user_id,
        "name": name,
        "first_name": first_name_from_full_name(name),
        "date_of_birth": patient.date_of_birth,
        "language": patient.language,
        "address": patient.address,
        "emergency_contact": patient.emergency_contact,
    }


def get_patient_for_user(db: Session, user_id: int) -> Patient | None:
    return (
        db.query(Patient)
        .filter(Patient.user_id == user_id)
        .first()
    )


@router.post(
    "/profile",
    response_model=PatientProfileResponse
)
def create_patient_profile(
    profile_data: PatientProfileCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    if current_user.role != "patient":
        raise HTTPException(
            status_code=403,
            detail="Only patients can create a patient profile"
        )

    existing_profile = get_patient_for_user(db, current_user.id)

    if existing_profile:
        raise HTTPException(
            status_code=400,
            detail="Patient profile already exists"
        )

    patient = Patient(
        user_id=current_user.id,
        date_of_birth=profile_data.date_of_birth,
        language=profile_data.language,
        address=profile_data.address,
        emergency_contact=profile_data.emergency_contact
    )

    db.add(patient)
    db.commit()
    db.refresh(patient)

    return serialize_patient_profile(patient, current_user)


def get_patient_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    row = (
        db.query(Patient, User)
        .join(User, Patient.user_id == User.id)
        .filter(Patient.user_id == current_user.id)
        .first()
    )

    if not row:
        raise HTTPException(
            status_code=404,
            detail="Patient profile not found"
        )

    patient, user = row
    return serialize_patient_profile(patient, user)


router.add_api_route(
    "/profile",
    get_patient_profile,
    methods=["GET"],
    response_model=PatientProfileResponse,
)
patient_router.add_api_route(
    "/profile",
    get_patient_profile,
    methods=["GET"],
    response_model=PatientProfileResponse,
)


@router.put("/profile", response_model=PatientProfileResponse)
def update_patient_profile(
    profile_data: PatientProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    patient = get_patient_for_user(db, current_user.id)

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient profile not found"
        )

    if profile_data.date_of_birth is not None:
        patient.date_of_birth = profile_data.date_of_birth

    if profile_data.language is not None:
        patient.language = profile_data.language

    if profile_data.address is not None:
        patient.address = profile_data.address

    if profile_data.emergency_contact is not None:
        patient.emergency_contact = profile_data.emergency_contact

    db.commit()
    db.refresh(patient)

    return serialize_patient_profile(patient, current_user)