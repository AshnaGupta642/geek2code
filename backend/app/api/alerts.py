from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database.database import get_db
from app.models.alert import Alert
from app.models.patient import Patient
from app.models.user import User
from app.schemas.alert import AlertCreate, AlertResponse
from app.models.family_member import FamilyMember
from app.core.dependencies import get_current_caregiver


router = APIRouter(
    prefix="/api/alerts",
    tags=["Alerts"]
)


@router.post(
    "/",
    response_model=AlertResponse
)
def create_alert(
    alert_data: AlertCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Only a patient can create an alert for their own account
    if current_user.role != "patient":
        raise HTTPException(
            status_code=403,
            detail="Only patients can create alerts"
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

    # Validate severity
    allowed_severities = ["LOW", "MEDIUM", "HIGH"]

    if alert_data.severity not in allowed_severities:
        raise HTTPException(
            status_code=400,
            detail="Invalid severity"
        )

    alert = Alert(
        patient_id=patient.id,
        alert_type=alert_data.alert_type,
        message=alert_data.message,
        severity=alert_data.severity,
        status="ACTIVE"
    )

    db.add(alert)
    db.commit()
    db.refresh(alert)

    return alert


@router.get(
    "/patient",
    response_model=list[AlertResponse]
)
def get_patient_alerts(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Only patients can access their own alerts
    if current_user.role != "patient":
        raise HTTPException(
            status_code=403,
            detail="Only patients can access their alerts"
        )

    patient = db.query(Patient).filter(
        Patient.user_id == current_user.id
    ).first()

    if patient is None:
        raise HTTPException(
            status_code=404,
            detail="Patient profile not found"
        )

    return db.query(Alert).filter(
        Alert.patient_id == patient.id
    ).order_by(
        Alert.created_at.desc()
    ).all()


@router.put(
    "/{alert_id}/resolve",
    response_model=AlertResponse
)
def resolve_alert(
    alert_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Only patients can resolve their own alerts for now
    if current_user.role != "patient":
        raise HTTPException(
            status_code=403,
            detail="Only patients can resolve alerts"
        )

    patient = db.query(Patient).filter(
        Patient.user_id == current_user.id
    ).first()

    if patient is None:
        raise HTTPException(
            status_code=404,
            detail="Patient profile not found"
        )

    alert = db.query(Alert).filter(
        Alert.id == alert_id,
        Alert.patient_id == patient.id
    ).first()

    if alert is None:
        raise HTTPException(
            status_code=404,
            detail="Alert not found"
        )

    alert.status = "RESOLVED"
    alert.resolved_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(alert)

    return alert
@router.get("/caregiver/{patient_id}")
def get_caregiver_alerts(
    patient_id: int,
    db: Session = Depends(get_db),
    caregiver: FamilyMember = Depends(get_current_caregiver)
):
    # Check that caregiver belongs to this patient
    if caregiver.patient_id != patient_id:
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to access this patient's alerts"
        )

    alerts = (
        db.query(Alert)
        .filter(Alert.patient_id == patient_id)
        .order_by(Alert.created_at.desc())
        .all()
    )

    return {
        "patient_id": patient_id,
        "alerts": alerts
    }