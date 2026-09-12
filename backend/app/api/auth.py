


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.user import User
from app.models.patient import Patient
from app.models.caregiver import Caregiver
from app.schemas.auth import (
    RegisterRequest,
    RegisterResponse,
    LoginRequest,
    LoginResponse
)
from app.core.security import hash_password, verify_password, create_access_token
from app.core.dependencies import get_current_user

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)


@router.post(
    "/register",
    response_model=RegisterResponse
)
def register(
    user_data: RegisterRequest,
    db: Session = Depends(get_db)
):

    # Check whether email already exists
    existing_user = (
        db.query(User)
        .filter(User.email == user_data.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    # Validate role
    if user_data.role not in ["patient", "caregiver"]:
        raise HTTPException(
            status_code=400,
            detail="Role must be patient or caregiver"
        )

    # Hash password
    hashed_password = hash_password(
        user_data.password
    )

    # Create user
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        password_hash=hashed_password,
        role=user_data.role
    )

    db.add(new_user)
    db.flush()

    # Matching profile rows are required after login:
    # patients for /api/family and /api/memories, caregivers for caregiver routes.
    if new_user.role == "patient":
        db.add(Patient(user_id=new_user.id))
    elif new_user.role == "caregiver":
        db.add(Caregiver(user_id=new_user.id))

    db.commit()
    db.refresh(new_user)

    return new_user

@router.post("/login", response_model=LoginResponse)
def login(user_data: LoginRequest, db: Session = Depends(get_db)):

    user = (
        db.query(User)
        .filter(User.email == user_data.email)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(user_data.password, user.password_hash):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        {
            "sub": str(user.id),
            "role": user.role
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "role": user.role
    }

@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "role": current_user.role
    }