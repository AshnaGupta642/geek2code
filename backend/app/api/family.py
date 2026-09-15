# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session

# from app.database.database import get_db
# from app.models.family_member import FamilyMember
# from app.models.patient import Patient
# from app.models.user import User
# from app.schemas.family import (
#     FamilyMemberCreate,
#     FamilyMemberUpdate,
#     FamilyMemberResponse
# )
# # change
# from app.core.dependencies import get_authorized_patient
# # change
# # from app.core.dependencies import get_current_user


# router = APIRouter(
#     prefix="/api/family",
#     tags=["Family"]
# )


# # ---------------------------------------------------
# # CREATE FAMILY MEMBER
# # ---------------------------------------------------

# @router.post(
#     "/",
#     response_model=FamilyMemberResponse
# )

# # def create_family_member(
# #     family_data: FamilyMemberCreate,
# #     current_user: User = Depends(get_current_user),
# #     db: Session = Depends(get_db)
# # ):



#     # Get patient profile
#     # patient = (
#     #     db.query(Patient)
#     #     .filter(Patient.user_id == current_user.id)
#     #     .first()
#     # )

#     # if not patient:
#     #     raise HTTPException(
#     #         status_code=404,
#     #         detail="Patient profile not found"
#     #     )
#     # if family_data.user_id is not None:

#     # change
# def create_family_member(
#     family_data: FamilyMemberCreate,
#     patient: Patient = Depends(get_authorized_patient),
#     db: Session = Depends(get_db)
# ):

#     if family_data.user_id is not None:
# # change


#         linked_user = db.query(User).filter(
#             User.id == family_data.user_id
#         ).first()

#         if not linked_user:
#             raise HTTPException(
#                 status_code=404,
#                 detail="User account not found"
#             )

#         if linked_user.role != "caregiver":
#             raise HTTPException(
#                 status_code=400,
#                 detail="User account must have caregiver role"
#             )

#         already_linked = db.query(FamilyMember).filter(
#             FamilyMember.user_id == family_data.user_id,
#             FamilyMember.is_active == True
#         ).first()

#         if already_linked:
#             raise HTTPException(
#                 status_code=400,
#                 detail="This user is already linked to a family member"
#             )
#     # Check if this member is being added as caregiver
#     if family_data.is_caregiver:

#         existing_caregiver = (
#             db.query(FamilyMember)
#             .filter(
#                 FamilyMember.patient_id == patient.id,
#                 FamilyMember.is_caregiver == True,
#                 FamilyMember.is_active == True
#             )
#             .first()
#         )

#         if existing_caregiver:
#             raise HTTPException(
#                 status_code=400,
#                 detail="This patient already has an active caregiver"
#             )

#     # Create family member
#     family_member = FamilyMember(
#         patient_id=patient.id,
#         user_id=family_data.user_id,
#         name=family_data.name,
#         relationship=family_data.relationship,
#         phone=family_data.phone,
#         photo_url=family_data.photo_url,
#         is_caregiver=family_data.is_caregiver
#     )

#     db.add(family_member)
#     db.commit()
#     db.refresh(family_member)

#     return family_member


# # ---------------------------------------------------
# # GET ALL FAMILY MEMBERS
# # ---------------------------------------------------

# @router.get(
#     "/",
#     response_model=list[FamilyMemberResponse]
# )
# # def get_family_members(
# #     current_user: User = Depends(get_current_user),
# #     db: Session = Depends(get_db)
# # ):

# #     patient = (
# #         db.query(Patient)
# #         .filter(Patient.user_id == current_user.id)
# #         .first()
# #     )

# #     if not patient:
# #         raise HTTPException(
# #             status_code=404,
# #             detail="Patient profile not found"
# #         )
# # change
# def get_family_members(
#     patient: Patient = Depends(get_authorized_patient),
#     db: Session = Depends(get_db)
# ):

   
# # change
#     family_members = (
#         db.query(FamilyMember)
#         .filter(
#             FamilyMember.patient_id == patient.id,
#             FamilyMember.is_active == True
#         )
#         .order_by(FamilyMember.created_at.desc())
#         .all()
#     )

#     return family_members


# # ---------------------------------------------------
# # GET SINGLE FAMILY MEMBER
# # ---------------------------------------------------

# @router.get(
#     "/{family_member_id}",
#     response_model=FamilyMemberResponse
# )
# # def get_family_member(
# #     family_member_id: int,
# #     current_user: User = Depends(get_current_user),
# #     db: Session = Depends(get_db)
# # ):

# #     patient = (
# #         db.query(Patient)
# #         .filter(Patient.user_id == current_user.id)
# #         .first()
# #     )

# #     if not patient:
# #         raise HTTPException(
# #             status_code=404,
# #             detail="Patient profile not found"
# #         )
# # change
# def get_family_member(
#     family_member_id: int,
#     patient: Patient = Depends(get_authorized_patient),
#     db: Session = Depends(get_db)
# ):

   
# # change
#     family_member = (
#         db.query(FamilyMember)
#         .filter(
#             FamilyMember.id == family_member_id,
#             FamilyMember.patient_id == patient.id,
#             FamilyMember.is_active == True
#         )
#         .first()
#     )

#     if not family_member:
#         raise HTTPException(
#             status_code=404,
#             detail="Family member not found"
#         )

#     return family_member


# # ---------------------------------------------------
# # UPDATE FAMILY MEMBER
# # ---------------------------------------------------

# @router.put(
#     "/{family_member_id}",
#     response_model=FamilyMemberResponse
# )
# def update_family_member(
#     family_member_id: int,
#     family_data: FamilyMemberUpdate,
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

#     family_member = (
#         db.query(FamilyMember)
#         .filter(
#             FamilyMember.id == family_member_id,
#             FamilyMember.patient_id == patient.id
#         )
#         .first()
#     )

#     if not family_member:
#         raise HTTPException(
#             status_code=404,
#             detail="Family member not found"
#         )

#     # If making this member the caregiver
#     if (
#         family_data.is_caregiver is True
#         and not family_member.is_caregiver
#     ):

#         existing_caregiver = (
#             db.query(FamilyMember)
#             .filter(
#                 FamilyMember.patient_id == patient.id,
#                 FamilyMember.is_caregiver == True,
#                 FamilyMember.is_active == True,
#                 FamilyMember.id != family_member_id
#             )
#             .first()
#         )

#         if existing_caregiver:
#             raise HTTPException(
#                 status_code=400,
#                 detail="This patient already has an active caregiver"
#             )

#         family_member.is_caregiver = True

#     # Remove caregiver role
#     if family_data.is_caregiver is False:
#         family_member.is_caregiver = False

#     # Update other fields
#     if family_data.name is not None:
#         family_member.name = family_data.name

#     if family_data.relationship is not None:
#         family_member.relationship = family_data.relationship

#     if family_data.phone is not None:
#         family_member.phone = family_data.phone

#     if family_data.photo_url is not None:
#         family_member.photo_url = family_data.photo_url

#     if family_data.is_active is not None:
#         family_member.is_active = family_data.is_active

#     db.commit()
#     db.refresh(family_member)

#     return family_member


# # ---------------------------------------------------
# # DELETE FAMILY MEMBER
# # SOFT DELETE
# # ---------------------------------------------------

# @router.delete("/{family_member_id}")
# def delete_family_member(
#     family_member_id: int,
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

#     family_member = (
#         db.query(FamilyMember)
#         .filter(
#             FamilyMember.id == family_member_id,
#             FamilyMember.patient_id == patient.id
#         )
#         .first()
#     )

#     if not family_member:
#         raise HTTPException(
#             status_code=404,
#             detail="Family member not found"
#         )

#     # Soft delete
#     family_member.is_active = False

#     # If deleted member was caregiver,
#     # automatically remove caregiver status
#     family_member.is_caregiver = False

#     db.commit()

#     return {
#         "success": True,
#         "message": "Family member removed successfully"
#     }


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.family_member import FamilyMember
from app.models.patient import Patient
from app.models.user import User
from app.schemas.family import (
    FamilyMemberCreate,
    FamilyMemberUpdate,
    FamilyMemberResponse
)
# from app.core.dependencies import get_current_user
from app.core.dependencies import get_authorized_patient, get_current_caregiver


router = APIRouter(
    prefix="/api/family",
    tags=["Family"]
)


# ---------------------------------------------------
# CREATE FAMILY MEMBER
# ---------------------------------------------------

@router.post(
    "/",
    response_model=FamilyMemberResponse
)
def create_family_member(
    family_data: FamilyMemberCreate,
    patient: Patient = Depends(get_authorized_patient),
    db: Session = Depends(get_db)
):

    if family_data.user_id is not None:

        linked_user = db.query(User).filter(
            User.id == family_data.user_id
        ).first()

        if not linked_user:
            raise HTTPException(
                status_code=404,
                detail="User account not found"
            )

        if linked_user.role != "caregiver":
            raise HTTPException(
                status_code=400,
                detail="User account must have caregiver role"
            )

        already_linked = db.query(FamilyMember).filter(
            FamilyMember.user_id == family_data.user_id,
            FamilyMember.is_active == True
        ).first()

        if already_linked:
            raise HTTPException(
                status_code=400,
                detail="This user is already linked to a family member"
            )
    # Check if this member is being added as caregiver
    if family_data.is_caregiver or family_data.is_emergency or family_data.is_primary:

        existing_caregiver = (
            db.query(FamilyMember)
            .filter(
                FamilyMember.patient_id == patient.id,
                FamilyMember.is_caregiver == True,
                FamilyMember.is_active == True
            )
            .first()
        )

        if existing_caregiver:
            raise HTTPException(
                status_code=400,
                detail="This patient already has an active caregiver"
            )

    # Create family member
    family_member = FamilyMember(
        patient_id=patient.id,
        user_id=family_data.user_id,
        name=family_data.name,
        relationship=family_data.relationship,
        phone=family_data.phone,
        photo_url=family_data.photo_url,
        is_caregiver=bool(
            family_data.is_caregiver
            or family_data.is_emergency
            or family_data.is_primary
        )
    )

    db.add(family_member)
    db.commit()
    db.refresh(family_member)

    return family_member


# ---------------------------------------------------
# GET ALL FAMILY MEMBERS
# ---------------------------------------------------

@router.get(
    "/",
    response_model=list[FamilyMemberResponse]
)
def get_family_members(
    patient: Patient = Depends(get_authorized_patient),
    db: Session = Depends(get_db)
):

    family_members = (
        db.query(FamilyMember)
        .filter(
            FamilyMember.patient_id == patient.id,
            FamilyMember.is_active == True
        )
        .order_by(FamilyMember.created_at.desc())
        .all()
    )

    return family_members


# ---------------------------------------------------
# GET SINGLE FAMILY MEMBER
# ---------------------------------------------------

@router.get(
    "/{family_member_id}",
    response_model=FamilyMemberResponse
)
def get_family_member(
    family_member_id: int,
    patient: Patient = Depends(get_authorized_patient),
    db: Session = Depends(get_db)
):

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

    return family_member


# ---------------------------------------------------
# UPDATE FAMILY MEMBER
# ---------------------------------------------------

@router.put(
    "/{family_member_id}",
    response_model=FamilyMemberResponse
)
def update_family_member(
    family_member_id: int,
    family_data: FamilyMemberUpdate,
    patient: Patient = Depends(get_authorized_patient),
    db: Session = Depends(get_db)
):

    family_member = (
        db.query(FamilyMember)
        .filter(
            FamilyMember.id == family_member_id,
            FamilyMember.patient_id == patient.id
        )
        .first()
    )

    if not family_member:
        raise HTTPException(
            status_code=404,
            detail="Family member not found"
        )

    # If making this member the caregiver
    if (
        family_data.is_caregiver is True
        or family_data.is_emergency is True
        or family_data.is_primary is True
    ) and not family_member.is_caregiver:

        existing_caregiver = (
            db.query(FamilyMember)
            .filter(
                FamilyMember.patient_id == patient.id,
                FamilyMember.is_caregiver == True,
                FamilyMember.is_active == True,
                FamilyMember.id != family_member_id
            )
            .first()
        )

        if existing_caregiver:
            raise HTTPException(
                status_code=400,
                detail="This patient already has an active caregiver"
            )

        family_member.is_caregiver = True

    # Remove caregiver role
    if family_data.is_caregiver is False:
        family_member.is_caregiver = False

    # Update other fields
    if family_data.name is not None:
        family_member.name = family_data.name

    if family_data.relationship is not None:
        family_member.relationship = family_data.relationship

    if family_data.phone is not None:
        family_member.phone = family_data.phone

    if family_data.photo_url is not None:
        family_member.photo_url = family_data.photo_url

    if family_data.is_active is not None:
        family_member.is_active = family_data.is_active

    db.commit()
    db.refresh(family_member)

    return family_member


# ---------------------------------------------------
# DELETE FAMILY MEMBER
# SOFT DELETE
# ---------------------------------------------------

@router.delete("/{family_member_id}")
def delete_family_member(
    family_member_id: int,
    patient: Patient = Depends(get_authorized_patient),
    db: Session = Depends(get_db)
):

    family_member = (
        db.query(FamilyMember)
        .filter(
            FamilyMember.id == family_member_id,
            FamilyMember.patient_id == patient.id
        )
        .first()
    )

    if not family_member:
        raise HTTPException(
            status_code=404,
            detail="Family member not found"
        )

    # Soft delete
    family_member.is_active = False

    # If deleted member was caregiver,
    # automatically remove caregiver status
    family_member.is_caregiver = False

    db.commit()

    return {
        "success": True,
        "message": "Family member removed successfully"
    }
# ---------------------------------------------------
# CAREGIVER GET PATIENT FAMILY MEMBERS
# ---------------------------------------------------

@router.get(
    "/caregiver/{patient_id}",
    response_model=list[FamilyMemberResponse]
)
def caregiver_get_family_members(
    patient_id: int,
    caregiver: FamilyMember = Depends(get_current_caregiver),
    db: Session = Depends(get_db)
):

    # Make sure caregiver belongs to this patient
    if caregiver.patient_id != patient_id:
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to view this patient's family members"
        )

    family_members = (
        db.query(FamilyMember)
        .filter(
            FamilyMember.patient_id == patient_id,
            FamilyMember.is_active == True
        )
        .order_by(FamilyMember.created_at.desc())
        .all()
    )

    return family_members