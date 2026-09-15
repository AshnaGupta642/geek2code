import json

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.face_profile import FaceProfile
from app.models.family_member import FamilyMember
from app.models.patient import Patient
from app.models.user import User
from app.core.dependencies import get_current_user

from app.schemas.face_recognition import (
    FaceProfileCreate,
    FaceProfileResponse,
    FaceRecognitionResult
)

from app.services.face_recognition_service import face_service


router = APIRouter(
    prefix="/api/face-recognition",
    tags=["Face Recognition"]
)


# =========================================================
# CREATE FACE PROFILE
# =========================================================

@router.post(
    "/profiles",
    response_model=FaceProfileResponse
)
def create_face_profile(
    data: FaceProfileCreate,
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


# =========================================================
# GET ALL FACE PROFILES
# =========================================================

@router.get(
    "/profiles",
    response_model=list[FaceProfileResponse]
)
def get_face_profiles(
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

    profiles = (
        db.query(FaceProfile)
        .filter(
            FaceProfile.patient_id == patient.id
        )
        .order_by(FaceProfile.created_at.asc())
        .all()
    )

    return profiles


# =========================================================
# GET SINGLE FACE PROFILE
# =========================================================

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


# =========================================================
# DELETE FACE PROFILE
# =========================================================

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


# =========================================================
# GENERATE / REGISTER FACE EMBEDDING
# =========================================================

@router.post(
    "/profiles/{family_member_id}/generate"
)
async def generate_face_embedding(
    family_member_id: int,
    photo: UploadFile = File(...),
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
            detail="Family member not found"
        )

    image_bytes = await photo.read()

    try:
        embedding = face_service.get_embedding(image_bytes)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    if embedding is None:
        raise HTTPException(
            status_code=400,
            detail="No face detected in the image"
        )

    profile = (
        db.query(FaceProfile)
        .filter(
            FaceProfile.family_member_id == family_member.id
        )
        .first()
    )

    if profile:
        profile.embedding_reference = json.dumps(
            embedding
        )
        profile.person_name = family_member.name

    else:
        profile = FaceProfile(
            patient_id=patient.id,
            family_member_id=family_member.id,
            person_name=family_member.name,
            embedding_reference=json.dumps(
                embedding
            )
        )

        db.add(profile)

    db.commit()
    db.refresh(profile)

    return {
        "message": "Face registered successfully",
        "profile_id": profile.id,
        "family_member_id": family_member.id,
        "person_name": family_member.name
    }


# =========================================================
# RECOGNIZE FACE
# =========================================================

@router.post(
    "/recognize",
    response_model=FaceRecognitionResult
)
async def recognize_face(
    photo: UploadFile = File(...),
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

    profiles = (
        db.query(FaceProfile)
        .filter(
            FaceProfile.patient_id == patient.id,
            FaceProfile.embedding_reference.isnot(None)
        )
        .all()
    )

    if not profiles:
        return FaceRecognitionResult(
            family_member_id=None,
            person_name=None,
            confidence=None,
            matched=False
        )

    image_bytes = await photo.read()

    try:
        query_embedding = face_service.get_embedding(
            image_bytes
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    if query_embedding is None:
        raise HTTPException(
            status_code=400,
            detail="No face detected"
        )

    result = face_service.find_best_match(
        query_embedding,
        profiles,
        threshold=0.40
    )

    return FaceRecognitionResult(**result)