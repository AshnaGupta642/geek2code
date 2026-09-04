from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.database.database import get_db
from app.models.user import User
from app.models.family_member import FamilyMember


security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = credentials.credentials

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


def get_current_caregiver(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # 1. User must have caregiver role
    if current_user.role != "caregiver":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Caregiver access required"
        )

    # 2. Find the family member linked to this caregiver account
    family_member = db.query(FamilyMember).filter(
        FamilyMember.user_id == current_user.id,
        FamilyMember.is_caregiver == True,
        FamilyMember.is_active == True
    ).first()

    # 3. Caregiver must actually be linked to a patient
    if family_member is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not linked to any patient as an active caregiver"
        )

    return family_member