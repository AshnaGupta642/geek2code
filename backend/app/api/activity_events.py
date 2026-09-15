from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database.database import get_db
from app.models.activity_event import ActivityEvent
from app.models.patient import Patient
from app.models.user import User
from app.schemas.activity_event import (
    ActivityEventCreate,
    ActivityEventResponse
)

router = APIRouter(
    prefix="/api/activity-events",
    tags=["Activity Events"]
)


@router.post(
    "/",
    response_model=ActivityEventResponse
)
def create_activity_event(
    event_data: ActivityEventCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Only patients can create activity events
    if current_user.role != "patient":
        raise HTTPException(
            status_code=403,
            detail="Only patients can create activity events"
        )

    # Find patient profile
    patient = db.query(Patient).filter(
        Patient.user_id == current_user.id
    ).first()

    if patient is None:
        raise HTTPException(
            status_code=404,
            detail="Patient profile not found"
        )

    # Create event
    activity_event = ActivityEvent(
        patient_id=patient.id,
        event_type=event_data.event_type,
        event_data=event_data.event_data,
        event_timestamp=event_data.event_timestamp
    )

    db.add(activity_event)
    db.commit()
    db.refresh(activity_event)

    return activity_event