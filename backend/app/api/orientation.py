from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.patient import Patient
from app.models.user import User
from app.core.dependencies import get_current_user
from app.schemas.orientation import OrientationResponse


router = APIRouter(
    prefix="/api/orientation",
    tags=["Orientation"]
)


@router.get(
    "/",
    response_model=OrientationResponse
)
def get_orientation(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Find patient belonging to the logged-in user
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

    # Get current UTC date and time
    now = datetime.now(timezone.utc)

    # Patient information directly from patients table
    language = patient.language or "en"
    location = patient.address

    # Build orientation message
    if location:
        orientation_message = (
            f"Today is {now.strftime('%A, %B %d, %Y')}. "
            f"The current time is {now.strftime('%I:%M %p')}. "
            f"You are in {location}."
        )
    else:
        orientation_message = (
            f"Today is {now.strftime('%A, %B %d, %Y')}. "
            f"The current time is {now.strftime('%I:%M %p')}."
        )

    return OrientationResponse(
        patient_id=patient.id,
        current_date=now.date(),
        current_time=now,
        day_of_week=now.strftime("%A"),
        language=language,
        location=location,
        orientation_message=orientation_message,
        status="ready"
    )