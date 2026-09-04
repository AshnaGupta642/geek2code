from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.models.emergency import EmergencyEvent
from app.models.patient import Patient
from app.models.user import User
from app.models.alert import Alert

from app.schemas.emergency import (
    EmergencyCreate,
    EmergencyResponse
)

from app.core.dependencies import get_current_user
from app.services.notification_service import notify_caregivers


router = APIRouter(
    prefix="/api/emergency",
    tags=["Emergency"]
)


# --------------------------------------------------
# TRIGGER SOS
# --------------------------------------------------

@router.post(
    "/sos",
    response_model=EmergencyResponse
)
def trigger_sos(
    emergency_data: EmergencyCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    # --------------------------------------------------
    # FIND PATIENT
    # --------------------------------------------------

    patient = db.query(Patient).filter(
        Patient.user_id == current_user.id
    ).first()

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient profile not found"
        )

    # --------------------------------------------------
    # SAVE EMERGENCY EVENT
    # --------------------------------------------------

    emergency = EmergencyEvent(
        patient_id=patient.id,
        trigger=emergency_data.trigger,
        latitude=emergency_data.latitude,
        longitude=emergency_data.longitude,
        timestamp=emergency_data.timestamp,
        status="ALERT_SENT"
    )

    db.add(emergency)
    db.commit()
    db.refresh(emergency)

    # --------------------------------------------------
    # CREATE CAREGIVER ALERT
    # --------------------------------------------------

    alert = Alert(
        patient_id=patient.id,
        alert_type="SOS",
        message="Emergency SOS has been triggered by the patient.",
        severity="HIGH",
        status="ACTIVE"
    )

    db.add(alert)
    db.commit()

    # --------------------------------------------------
    # NOTIFY CAREGIVERS
    # --------------------------------------------------

    notify_caregivers(
        db=db,
        patient_id=patient.id,
        notification_type="SOS",
        title="Emergency Alert",
        message="The patient has triggered an SOS emergency alert."
    )

    # --------------------------------------------------
    # RESPONSE
    # --------------------------------------------------

    return {
        "success": True,
        "event_id": emergency.id,
        "status": "ALERT_SENT",
        "caregiver_notified": True
    }