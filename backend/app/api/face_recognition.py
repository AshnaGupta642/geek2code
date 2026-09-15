from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.face_profile import FaceProfile
from app.models.family_member import FamilyMember
from app.models.patient import Patient
from app.models.user import User
from app.core.dependencies import get_current_user
from app.schemas.face_recognition import (
    FaceProfileCreate,
    FaceProfileResponse
)


router = APIRouter(
    prefix="/api/face-recognition",
    tags=["Face Recognition"]
)


@router.post(
    "/profiles",
    response_model=FaceProfileResponse
)
def create_face_profile(
    data: FaceProfileCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Find current patient's profile
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

    # Verify family member belongs to this patient
    family_member = (
        db.query(FamilyMember)
        .filter(
            FamilyMember.id == data.family_member_id,
            FamilyMember.patient_id == patient.id,
            FamilyMember.is_active == True
        )
        .first()
    )

    if not family_member:
        raise HTTPException(
            status_code=404,
            detail="Family member not found"
        )

    # Prevent duplicate face profile
    existing_profile = (
        db.query(FaceProfile)
        .filter(
            FaceProfile.family_member_id == family_member.id
        )
        .first()
    )

    if existing_profile:
        raise HTTPException(
            status_code=409,
            detail="Face profile already exists for this family member"
        )

    profile = FaceProfile(
        patient_id=patient.id,
        family_member_id=family_member.id,
        person_name=family_member.name,
        face_image_url=data.face_image_url,
        embedding_reference=data.embedding_reference
    )

    db.add(profile)
    db.commit()
    db.refresh(profile)

    return profile


@router.get(
    "/profiles",
    response_model=list[FaceProfileResponse]
)
def get_face_profiles(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Find current patient
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

    profiles = (
        db.query(FaceProfile)
        .filter(
            FaceProfile.patient_id == patient.id
        )
        .order_by(FaceProfile.created_at.asc())
        .all()
    )

    return profiles


@router.get(
    "/profiles/{profile_id}",
    response_model=FaceProfileResponse
)
def get_face_profile(
    profile_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
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

    profile = (
        db.query(FaceProfile)
        .filter(
            FaceProfile.id == profile_id,
            FaceProfile.patient_id == patient.id
        )
        .first()
    )

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Face profile not found"
        )

    return profile


@router.delete(
    "/profiles/{profile_id}"
)
def delete_face_profile(
    profile_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
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

    profile = (
        db.query(FaceProfile)
        .filter(
            FaceProfile.id == profile_id,
            FaceProfile.patient_id == patient.id
        )
        .first()
    )

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Face profile not found"
        )

    db.delete(profile)
    db.commit()

    return {
        "message": "Face profile deleted successfully",
        "profile_id": profile_id
    }