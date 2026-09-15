from fastapi import Depends, Header, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.models.patient import Patient

from app.core.config import settings
from app.database.database import get_db
from app.models.user import User
from app.models.family_member import FamilyMember
from app.models.caregiver import Caregiver
from app.models.patient_caregiver import PatientCaregiver


security = HTTPBearer(auto_error=False)


def _extract_bearer_token(
    credentials: HTTPAuthorizationCredentials | None,
    authorization: str | None,
) -> str | None:
    token = None
    if credentials and credentials.credentials:
        token = credentials.credentials
    elif authorization:
        token = authorization.strip()

    if not token:
        return None

    while token.lower().startswith("bearer "):
        token = token[7:].strip()

    return token or None


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
    authorization: str | None = Header(default=None),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = _extract_bearer_token(credentials, authorization)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise credentials_exception

        user_id = int(user_id)

    except (JWTError, ValueError):
        raise credentials_exception

    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise credentials_exception

    return user


# def get_current_caregiver(
#     current_user: User = Depends(get_current_user),
#     db: Session = Depends(get_db)
# ):
#     # 1. User must have caregiver role
#     if current_user.role != "caregiver":
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Caregiver access required"
#         )

#     # 2. Find the family member linked to this caregiver account
#     family_member = db.query(FamilyMember).filter(
#         FamilyMember.user_id == current_user.id,
#         FamilyMember.is_caregiver == True,
#         FamilyMember.is_active == True
#     ).first()

#     # 3. Caregiver must actually be linked to a patient
#     if family_member is None:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="You are not linked to any patient as an active caregiver"
#         )

#     return family_member

def get_current_caregiver(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != "caregiver":
        raise HTTPException(
            status_code=403,
            detail="Caregiver access required"
        )

    caregiver = db.query(Caregiver).filter(
        Caregiver.user_id == current_user.id
    ).first()

    if caregiver is None:
        caregiver = Caregiver(user_id=current_user.id)
        db.add(caregiver)
        db.commit()
        db.refresh(caregiver)

    relationship = db.query(PatientCaregiver).filter(
        PatientCaregiver.caregiver_id == caregiver.id
    ).first()

    patient_id = relationship.patient_id if relationship is not None else None

    if patient_id is None:
        family_member = db.query(FamilyMember).filter(
            FamilyMember.user_id == current_user.id,
            FamilyMember.is_active == True
        ).first()
        if family_member is None:
            raise HTTPException(
                status_code=403,
                detail="You are not linked to any patient"
            )
        patient_id = family_member.patient_id

    caregiver.patient_id = patient_id
    return caregiver

# change

# def get_authorized_patient(
#     current_user: User = Depends(get_current_user),
#     db: Session = Depends(get_db)
# ) -> Patient:
#     """
#     Resolves the Patient record the current user is allowed to act on.

#     - If the logged-in user IS the patient, returns their own Patient row.
#     - If the logged-in user is a caregiver, returns the single Patient
#       they are linked to via their active FamilyMember record.
#     - Anyone else is rejected.
#     """

#     if current_user.role == "patient":
#         patient = db.query(Patient).filter(
#             Patient.user_id == current_user.id
#         ).first()

#         if patient is None:
#             raise HTTPException(
#                 status_code=404,
#                 detail="Patient profile not found"
#             )

#         return patient

    # if current_user.role == "caregiver":
    #     family_member = db.query(FamilyMember).filter(
    #         FamilyMember.user_id == current_user.id,
    #         FamilyMember.is_caregiver == True,
    #         FamilyMember.is_active == True
    #     ).first()

    #     if family_member is None:
    #         raise HTTPException(
    #             status_code=403,
    #             detail="You are not linked to any patient as an active caregiver"
    #         )

    #     patient = db.query(Patient).filter(
    #         Patient.id == family_member.patient_id
    #     ).first()

    #     if patient is None:
    #         raise HTTPException(
    #             status_code=404,
    #             detail="Linked patient profile not found"
    #         )

    #     return patient

    # raise HTTPException(
    #     status_code=403,
    #     detail="You are not authorized to access patient data"
    # )
# changee

def get_authorized_patient(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Patient:

    # -----------------------------
    # PATIENT
    # -----------------------------

    if current_user.role == "patient":

        patient = db.query(Patient).filter(
            Patient.user_id == current_user.id
        ).first()

        if patient is None:
            patient = Patient(user_id=current_user.id)
            db.add(patient)
            db.commit()
            db.refresh(patient)

        return patient

    # -----------------------------
    # CAREGIVER
    # -----------------------------

    if current_user.role == "caregiver":

        caregiver = db.query(Caregiver).filter(
            Caregiver.user_id == current_user.id
        ).first()

        if caregiver is None:
            caregiver = Caregiver(user_id=current_user.id)
            db.add(caregiver)
            db.commit()
            db.refresh(caregiver)

        relationship = db.query(PatientCaregiver).filter(
            PatientCaregiver.caregiver_id == caregiver.id
        ).first()

        patient = None
        if relationship is not None:
            patient = db.query(Patient).filter(
                Patient.id == relationship.patient_id
            ).first()

        if patient is None:
            family_member = db.query(FamilyMember).filter(
                FamilyMember.user_id == current_user.id,
                FamilyMember.is_active == True
            ).first()
            if family_member is not None:
                patient = db.query(Patient).filter(
                    Patient.id == family_member.patient_id
                ).first()

        if patient is None:
            raise HTTPException(
                status_code=403,
                detail="You are not linked to any patient"
            )

        return patient

    # -----------------------------
    # EVERYTHING ELSE
    # -----------------------------

    raise HTTPException(
        status_code=403,
        detail="You are not authorized to access patient data"
    )