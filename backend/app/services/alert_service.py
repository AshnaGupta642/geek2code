from datetime import datetime, timezone, timedelta

from sqlalchemy.orm import Session

from app.models.alert import Alert
from app.models.reminder_history import ReminderHistory

from app.services.notification_service import notify_caregivers


def check_missed_reminder_alert(
    patient_id: int,
    db: Session
):
    """
    Checks whether a patient has missed 3 or more reminders
    recently and creates a caregiver alert if necessary.

    If 3 or more reminders are missed within the last 7 days:
    1. Creates a MISSED_REMINDERS alert.
    2. Sends a notification to all active caregivers.
    """

    # Current UTC time
    now = datetime.now(timezone.utc)

    # --------------------------------------------------
    # CHECK LAST 7 DAYS
    # --------------------------------------------------

    seven_days_ago = now - timedelta(days=7)

    recent_history = (
        db.query(ReminderHistory)
        .filter(
            ReminderHistory.patient_id == patient_id,
            ReminderHistory.scheduled_at >= seven_days_ago,
            ReminderHistory.status == "MISSED"
        )
        .order_by(
            ReminderHistory.scheduled_at.desc()
        )
        .all()
    )

    missed_count = len(recent_history)

    # --------------------------------------------------
    # REQUIRE AT LEAST 3 MISSED REMINDERS
    # --------------------------------------------------

    if missed_count < 3:
        return None

    # --------------------------------------------------
    # CHECK IF ACTIVE ALERT ALREADY EXISTS
    # --------------------------------------------------

    existing_alert = (
        db.query(Alert)
        .filter(
            Alert.patient_id == patient_id,
            Alert.alert_type == "MISSED_REMINDERS",
            Alert.status == "ACTIVE"
        )
        .first()
    )

    # Avoid creating duplicate alerts/notifications
    if existing_alert:
        return existing_alert

    # --------------------------------------------------
    # CREATE MISSED REMINDER ALERT
    # --------------------------------------------------

    alert = Alert(
        patient_id=patient_id,
        alert_type="MISSED_REMINDERS",
        message=(
            f"Patient has missed {missed_count} reminders "
            f"in the last 7 days."
        ),
        severity="MEDIUM",
        status="ACTIVE"
    )

    db.add(alert)
    db.commit()
    db.refresh(alert)

    # --------------------------------------------------
    # NOTIFY ALL ACTIVE CAREGIVERS
    # --------------------------------------------------

    notify_caregivers(
        db=db,
        patient_id=patient_id,
        notification_type="MISSED_REMINDERS",
        title="Missed Medicine Reminder",
        message=(
            f"The patient has missed {missed_count} reminders "
            f"in the last 7 days."
        )
    )

    # --------------------------------------------------
    # RETURN CREATED ALERT
    # --------------------------------------------------

    return alert