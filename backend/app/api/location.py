from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from math import radians, sin, cos, sqrt, atan2

from app.database.database import get_db

from app.models.location import Location
from app.models.patient import Patient
from app.models.user import User
from app.models.family_member import FamilyMember
from app.models.safe_zone import SafeZone
from app.models.alert import Alert
from app.schemas.location import LocationCreate

from app.core.dependencies import (
    get_current_user,
    get_current_caregiver
)

from app.services.notification_service import notify_caregivers


router = APIRouter(
    prefix="/api/location",
    tags=["Location"]
)


# --------------------------------------------------
# CALCULATE DISTANCE BETWEEN TWO GPS COORDINATES
# --------------------------------------------------

def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculate distance between two GPS coordinates
    in meters using the Haversine formula.
    """

    R = 6371000  # Earth radius in meters

    lat1 = radians(lat1)
    lat2 = radians(lat2)

    dlat = lat2 - lat1
    dlon = radians(lon2 - lon1)

    a = (
        sin(dlat / 2) ** 2
        + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    )

    c = 2 * atan2(
        sqrt(a),
        sqrt(1 - a)
    )

    return R * c


# --------------------------------------------------
# SAVE PATIENT LOCATION
# --------------------------------------------------

@router.post("/")
def save_location(
    location_data: LocationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    # Find patient associated with logged-in user
    patient = db.query(Patient).filter(
        Patient.user_id == current_user.id
    ).first()

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient profile not found"
        )

    # --------------------------------------------------
    # SAVE LOCATION
    # --------------------------------------------------

    location = Location(
        patient_id=patient.id,
        latitude=location_data.latitude,
        longitude=location_data.longitude,
        accuracy_meters=location_data.accuracy_meters,
        timestamp=location_data.timestamp
    )

    db.add(location)
    db.commit()
    db.refresh(location)

    # --------------------------------------------------
    # CHECK SAFE ZONE
    # --------------------------------------------------

    safe_zones = (
        db.query(SafeZone)
        .filter(
            SafeZone.patient_id == patient.id,
            SafeZone.is_active == True
        )
        .all()
    )

    inside_safe_zone = False
    safe_zone_id = None

    # Check patient's location against every active safe zone
    for zone in safe_zones:

        distance = calculate_distance(
            location_data.latitude,
            location_data.longitude,
            zone.latitude,
            zone.longitude
        )

        if distance <= zone.radius_meters:

            inside_safe_zone = True
            safe_zone_id = zone.id

            break

    # --------------------------------------------------
    # CREATE ALERT + NOTIFY CAREGIVERS
    # IF PATIENT IS OUTSIDE SAFE ZONE
    # --------------------------------------------------

    if not inside_safe_zone and safe_zones:

        alert = Alert(
            patient_id=patient.id,
            alert_type="SAFE_ZONE_EXIT",
            message="Patient is outside the configured safe zone.",
            severity="HIGH",
            status="ACTIVE"
        )

        db.add(alert)
        db.commit()

        # Notify all active caregivers
        notify_caregivers(
            db=db,
            patient_id=patient.id,
            notification_type="SAFE_ZONE_EXIT",
            title="Safe Zone Alert",
            message="The patient has exited the configured safe zone."
        )

    # --------------------------------------------------
    # RESPONSE
    # --------------------------------------------------

    return {
        "success": True,
        "inside_safe_zone": inside_safe_zone,
        "safe_zone_id": safe_zone_id
    }


# --------------------------------------------------
# GET PATIENT LATEST LOCATION — CAREGIVER
# --------------------------------------------------

@router.get(
    "/patient/{patient_id}"
)
def get_latest_location(
    patient_id: int,
    caregiver: FamilyMember = Depends(get_current_caregiver),
    db: Session = Depends(get_db)
):

    # Check caregiver belongs to this patient
    if caregiver.patient_id != patient_id:

        raise HTTPException(
            status_code=403,
            detail="You are not authorized to access this patient's location"
        )

    # Get latest location
    location = (
        db.query(Location)
        .filter(
            Location.patient_id == patient_id
        )
        .order_by(
            Location.timestamp.desc()
        )
        .first()
    )

    # No location available
    if not location:

        return {
            "patient_id": patient_id,
            "location": None,
            "last_seen": None
        }

    # Return latest location
    return {
        "patient_id": patient_id,
        "location": {
            "latitude": location.latitude,
            "longitude": location.longitude,
            "accuracy_meters": location.accuracy_meters,
            "updated_at": location.timestamp
        },
        "last_seen": location.timestamp
    }


# --------------------------------------------------
# GET PATIENT LOCATION HISTORY — CAREGIVER
# --------------------------------------------------

@router.get(
    "/patient/{patient_id}/history"
)
def get_location_history(
    patient_id: int,
    caregiver: FamilyMember = Depends(get_current_caregiver),
    db: Session = Depends(get_db)
):

    # Check caregiver belongs to this patient
    if caregiver.patient_id != patient_id:

        raise HTTPException(
            status_code=403,
            detail="You are not authorized to access this patient's location history"
        )

    # Get all locations
    locations = (
        db.query(Location)
        .filter(
            Location.patient_id == patient_id
        )
        .order_by(
            Location.timestamp.desc()
        )
        .all()
    )

    return {
        "patient_id": patient_id,
        "locations": [
            {
                "latitude": location.latitude,
                "longitude": location.longitude,
                "accuracy_meters": location.accuracy_meters,
                "timestamp": location.timestamp
            }
            for location in locations
        ]
    }