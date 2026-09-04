from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.notification import Notification
from app.core.dependencies import get_current_user
from app.schemas.notification import NotificationResponse
from app.services.notification_service import (
    notify_patient,
    notify_caregivers
)
from app.models.patient import Patient

router = APIRouter(
    prefix="/api/notifications",
    tags=["Notifications"]
)


# Get all notifications of logged-in user
@router.get("/", response_model=list[NotificationResponse])
def get_my_notifications(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    notifications = (
        db.query(Notification)
        .filter(Notification.user_id == current_user.id)
        .order_by(Notification.created_at.desc())
        .all()
    )

    return notifications


# Get only unread notifications
@router.get("/unread", response_model=list[NotificationResponse])
def get_unread_notifications(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    notifications = (
        db.query(Notification)
        .filter(
            Notification.user_id == current_user.id,
            Notification.is_read == False
        )
        .order_by(Notification.created_at.desc())
        .all()
    )

    return notifications


# Get unread notification count
@router.get("/unread-count")
def get_unread_count(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    count = (
        db.query(Notification)
        .filter(
            Notification.user_id == current_user.id,
            Notification.is_read == False
        )
        .count()
    )

    return {
        "unread_count": count
    }


# Mark one notification as read
@router.put("/{notification_id}/read")
def mark_notification_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    notification = (
        db.query(Notification)
        .filter(
            Notification.id == notification_id,
            Notification.user_id == current_user.id
        )
        .first()
    )

    if not notification:
        raise HTTPException(
            status_code=404,
            detail="Notification not found."
        )

    notification.is_read = True
    notification.read_at = datetime.now(timezone.utc)

    db.commit()

    return {
        "message": "Notification marked as read.",
        "notification_id": notification.id
    }


# Mark all notifications as read
@router.put("/read-all")
def mark_all_notifications_read(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    notifications = (
        db.query(Notification)
        .filter(
            Notification.user_id == current_user.id,
            Notification.is_read == False
        )
        .all()
    )

    now = datetime.now(timezone.utc)

    for notification in notifications:
        notification.is_read = True
        notification.read_at = now

    db.commit()

    return {
        "message": "All notifications marked as read.",
        "updated_count": len(notifications)
    }
@router.post("/test")
def test_notification(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    patient = (
        db.query(Patient)
        .filter(Patient.user_id == current_user.id)
        .first()
    )

    if not patient:
        raise HTTPException(
            status_code=403,
            detail="Only patients can run this test."
        )

    patient_notification = notify_patient(
        db=db,
        patient_id=patient.id,
        notification_type="TEST",
        title="Memora Test Notification",
        message="Notification service is working."
    )

    caregiver_notifications = notify_caregivers(
        db=db,
        patient_id=patient.id,
        notification_type="TEST_CAREGIVER",
        title="Memora Caregiver Test",
        message="Caregiver notification service is working."
    )

    return {
        "patient_notification_id": (
            patient_notification.id
            if patient_notification
            else None
        ),
        "caregiver_notifications": [
            notification.id
            for notification in caregiver_notifications
        ]
    }