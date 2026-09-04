from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.models.user import User
from app.models.patient import Patient
from app.models.reminder import Reminder
from app.models.reminder_history import ReminderHistory

from app.schemas.reminder_history import (
    ReminderEventCreate,
    ReminderHistoryResponse,
    ReminderAdherenceResponse
)

from app.core.dependencies import get_current_user
from app.models.family_member import FamilyMember
from app.core.dependencies import get_current_caregiver
from app.services.alert_service import check_missed_reminder_alert

router = APIRouter(
    prefix="/api/reminders",
    tags=["Reminder History"]
)


# --------------------------------------------------
# RECORD REMINDER EVENT
# --------------------------------------------------

@router.post(
    "/event",
    response_model=ReminderHistoryResponse
)
def record_reminder_event(
    event_data: ReminderEventCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    patient = db.query(Patient).filter(
        Patient.user_id == current_user.id
    ).first()

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient profile not found"
        )

    # Check reminder ownership
    reminder = db.query(Reminder).filter(
        Reminder.id == event_data.reminder_id,
        Reminder.patient_id == patient.id
    ).first()

    if not reminder:
        raise HTTPException(
            status_code=404,
            detail="Reminder not found"
        )

    # Validate status
    allowed_statuses = [
        "COMPLETED",
        "MISSED",
        "SKIPPED",
        "PENDING"
    ]

    if event_data.status not in allowed_statuses:
        raise HTTPException(
            status_code=400,
            detail="Invalid reminder status"
        )

    now = datetime.now(timezone.utc)

    # Create history record
    history = ReminderHistory(
        reminder_id=reminder.id,
        patient_id=patient.id,
        scheduled_at=datetime.combine(
            now.date(),
            reminder.scheduled_time,
            tzinfo=timezone.utc
        ),
        completed_at=(
            now
            if event_data.status == "COMPLETED"
            else None
        ),
        status=event_data.status
    )

    db.add(history)
    db.commit()
    db.refresh(history)
    # Check whether repeated missed reminders
    # should trigger a caregiver alert.
    if event_data.status == "MISSED":
        check_missed_reminder_alert(
            patient_id=patient.id,
            db=db
        )

    return history


# --------------------------------------------------
# GET REMINDER HISTORY
# --------------------------------------------------

@router.get(
    "/history",
    response_model=list[ReminderHistoryResponse]
)
def get_reminder_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    patient = db.query(Patient).filter(
        Patient.user_id == current_user.id
    ).first()

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient profile not found"
        )

    history = db.query(ReminderHistory).filter(
        ReminderHistory.patient_id == patient.id
    ).order_by(
        ReminderHistory.scheduled_at.desc()
    ).all()

    return history


# --------------------------------------------------
# GET ADHERENCE
# --------------------------------------------------

@router.get(
    "/adherence",
    response_model=ReminderAdherenceResponse
)
def get_reminder_adherence(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    patient = db.query(Patient).filter(
        Patient.user_id == current_user.id
    ).first()

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient profile not found"
        )

    history = db.query(ReminderHistory).filter(
        ReminderHistory.patient_id == patient.id
    ).all()

    total = len(history)

    completed = sum(
        1 for item in history
        if item.status == "COMPLETED"
    )

    missed = sum(
        1 for item in history
        if item.status == "MISSED"
    )

    skipped = sum(
        1 for item in history
        if item.status == "SKIPPED"
    )

    pending = sum(
        1 for item in history
        if item.status == "PENDING"
    )

    # Adherence is based on completed reminders
    # out of reminders that were actually due.
    due = completed + missed + skipped

    if due == 0:
        adherence_percentage = 0.0
    else:
        adherence_percentage = round(
            (completed / due) * 100,
            2
        )

    return {
        "total": total,
        "completed": completed,
        "missed": missed,
        "skipped": skipped,
        "pending": pending,
        "adherence_percentage": adherence_percentage
    }
# --------------------------------------------------
# CAREGIVER GET PATIENT ADHERENCE
# --------------------------------------------------

@router.get(
    "/caregiver/{patient_id}/adherence",
    response_model=ReminderAdherenceResponse
)
def caregiver_get_patient_adherence(
    patient_id: int,
    caregiver: FamilyMember = Depends(get_current_caregiver),
    db: Session = Depends(get_db)
):

    # Make sure caregiver belongs to this patient
    if caregiver.patient_id != patient_id:
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to view this patient's adherence"
        )

    history = db.query(ReminderHistory).filter(
        ReminderHistory.patient_id == patient_id
    ).all()

    total = len(history)

    completed = sum(
        1 for item in history
        if item.status == "COMPLETED"
    )

    missed = sum(
        1 for item in history
        if item.status == "MISSED"
    )

    skipped = sum(
        1 for item in history
        if item.status == "SKIPPED"
    )

    pending = sum(
        1 for item in history
        if item.status == "PENDING"
    )

    # Pending reminders are not included
    # because they are not completed/missed/skipped yet.
    due = completed + missed + skipped

    if due == 0:
        adherence_percentage = 0.0
    else:
        adherence_percentage = round(
            (completed / due) * 100,
            2
        )

    return {
        "total": total,
        "completed": completed,
        "missed": missed,
        "skipped": skipped,
        "pending": pending,
        "adherence_percentage": adherence_percentage
    }