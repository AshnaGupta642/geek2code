from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.medicine import Medicine
from app.models.patient import Patient
from app.models.user import User
from app.schemas.medicine import (
    MedicineCreate,
    MedicineUpdate,
    MedicineResponse
)
from app.core.dependencies import get_current_user


router = APIRouter(
    prefix="/api/medicines",
    tags=["Medicines"]
)


# ---------------------------------------------------
# CREATE MEDICINE
# ---------------------------------------------------

@router.post(
    "/",
    response_model=MedicineResponse
)
def create_medicine(
    medicine_data: MedicineCreate,
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

    medicine = Medicine(
        patient_id=patient.id,
        name=medicine_data.name,
        dosage=medicine_data.dosage,
        instructions=medicine_data.instructions,
        start_date=medicine_data.start_date,
        end_date=medicine_data.end_date
    )

    db.add(medicine)
    db.commit()
    db.refresh(medicine)

    return medicine


# ---------------------------------------------------
# GET ALL MEDICINES
# ---------------------------------------------------

@router.get(
    "/",
    response_model=list[MedicineResponse]
)
def get_medicines(
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

    medicines = (
        db.query(Medicine)
        .filter(
            Medicine.patient_id == patient.id,
            Medicine.is_active == True
        )
        .order_by(Medicine.created_at.desc())
        .all()
    )

    return medicines


# ---------------------------------------------------
# GET SINGLE MEDICINE
# ---------------------------------------------------

@router.get(
    "/{medicine_id}",
    response_model=MedicineResponse
)
def get_medicine(
    medicine_id: int,
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

    medicine = (
        db.query(Medicine)
        .filter(
            Medicine.id == medicine_id,
            Medicine.patient_id == patient.id,
            Medicine.is_active == True
        )
        .first()
    )

    if not medicine:
        raise HTTPException(
            status_code=404,
            detail="Medicine not found"
        )

    return medicine


# ---------------------------------------------------
# UPDATE MEDICINE
# ---------------------------------------------------

@router.put(
    "/{medicine_id}",
    response_model=MedicineResponse
)
def update_medicine(
    medicine_id: int,
    medicine_data: MedicineUpdate,
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

    medicine = (
        db.query(Medicine)
        .filter(
            Medicine.id == medicine_id,
            Medicine.patient_id == patient.id
        )
        .first()
    )

    if not medicine:
        raise HTTPException(
            status_code=404,
            detail="Medicine not found"
        )

    if medicine_data.name is not None:
        medicine.name = medicine_data.name

    if medicine_data.dosage is not None:
        medicine.dosage = medicine_data.dosage

    if medicine_data.instructions is not None:
        medicine.instructions = medicine_data.instructions

    if medicine_data.start_date is not None:
        medicine.start_date = medicine_data.start_date

    if medicine_data.end_date is not None:
        medicine.end_date = medicine_data.end_date

    if medicine_data.is_active is not None:
        medicine.is_active = medicine_data.is_active

    db.commit()
    db.refresh(medicine)

    return medicine


# ---------------------------------------------------
# DELETE / DEACTIVATE MEDICINE
# ---------------------------------------------------

@router.delete("/{medicine_id}")
def delete_medicine(
    medicine_id: int,
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

    medicine = (
        db.query(Medicine)
        .filter(
            Medicine.id == medicine_id,
            Medicine.patient_id == patient.id
        )
        .first()
    )

    if not medicine:
        raise HTTPException(
            status_code=404,
            detail="Medicine not found"
        )

    # Soft delete
    medicine.is_active = False

    db.commit()

    return {
        "success": True,
        "message": "Medicine removed successfully"
    }