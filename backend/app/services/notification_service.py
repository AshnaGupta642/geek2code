from sqlalchemy.orm import Session

from app.models.notification import Notification
from app.models.patient import Patient
from app.models.family_member import FamilyMember


def create_notification(
    db: Session,
    user_id: int,
    notification_type: str,
    title: str,
    message: str,
    patient_id: int | None = None
):
    """
    Create a notification for a specific user.
    """

    notification = Notification(
        user_id=user_id,
        patient_id=patient_id,
        notification_type=notification_type,
        title=title,
        message=message,
        is_read=False
    )

    db.add(notification)
    db.commit()
    db.refresh(notification)

    return notification


def notify_patient(
    db: Session,
    patient_id: int,
    notification_type: str,
    title: str,
    message: str
):
    """
    Send notification to the patient.
    """

    patient = (
        db.query(Patient)
        .filter(Patient.id == patient_id)
        .first()
    )

    if not patient:
        return None

    return create_notification(
        db=db,
        user_id=patient.user_id,
        patient_id=patient_id,
        notification_type=notification_type,
        title=title,
        message=message
    )


def notify_caregivers(
    db: Session,
    patient_id: int,
    notification_type: str,
    title: str,
    message: str
):
    """
    Send notification to all active caregivers
    associated with a patient.
    """

    caregivers = (
        db.query(FamilyMember)
        .filter(
            FamilyMember.patient_id == patient_id,
            FamilyMember.is_caregiver == True,
            FamilyMember.is_active == True,
            FamilyMember.user_id.isnot(None)
        )
        .all()
    )

    notifications = []

    for caregiver in caregivers:

        notification = create_notification(
            db=db,
            user_id=caregiver.user_id,
            patient_id=patient_id,
            notification_type=notification_type,
            title=title,
            message=message
        )

        notifications.append(notification)

    return notifications