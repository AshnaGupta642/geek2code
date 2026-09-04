from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.safe_zone import SafeZone
from app.models.family_member import FamilyMember
from app.schemas.safe_zone import (
    SafeZoneCreate,
    SafeZoneUpdate,
    SafeZoneResponse
)
from app.core.dependencies import get_current_caregiver


router = APIRouter(
    prefix="/api/safe-zones",
    tags=["Safe Zones"]
)


# --------------------------------------------------
# CREATE SAFE ZONE — CAREGIVER
# --------------------------------------------------

@router.post(
    "/{patient_id}",
    response_model=SafeZoneResponse
)
def create_safe_zone(
    patient_id: int,
    zone_data: SafeZoneCreate,
    caregiver: FamilyMember = Depends(get_current_caregiver),
    db: Session = Depends(get_db)
):

    if caregiver.patient_id != patient_id:
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to manage this patient's safe zones"
        )

    safe_zone = SafeZone(
        patient_id=patient_id,
        name=zone_data.name,
        latitude=zone_data.latitude,
        longitude=zone_data.longitude,
        radius_meters=zone_data.radius_meters,
        is_active=True
    )

    db.add(safe_zone)
    db.commit()
    db.refresh(safe_zone)

    return safe_zone


# --------------------------------------------------
# GET SAFE ZONES — CAREGIVER
# --------------------------------------------------

@router.get(
    "/{patient_id}",
    response_model=list[SafeZoneResponse]
)
def get_safe_zones(
    patient_id: int,
    caregiver: FamilyMember = Depends(get_current_caregiver),
    db: Session = Depends(get_db)
):

    if caregiver.patient_id != patient_id:
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to access this patient's safe zones"
        )

    return db.query(SafeZone).filter(
        SafeZone.patient_id == patient_id,
        SafeZone.is_active == True
    ).all()


# --------------------------------------------------
# UPDATE SAFE ZONE — CAREGIVER
# --------------------------------------------------

@router.put(
    "/{patient_id}/{zone_id}",
    response_model=SafeZoneResponse
)
def update_safe_zone(
    patient_id: int,
    zone_id: int,
    zone_data: SafeZoneUpdate,
    caregiver: FamilyMember = Depends(get_current_caregiver),
    db: Session = Depends(get_db)
):

    if caregiver.patient_id != patient_id:
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to manage this patient's safe zones"
        )

    safe_zone = db.query(SafeZone).filter(
        SafeZone.id == zone_id,
        SafeZone.patient_id == patient_id
    ).first()

    if not safe_zone:
        raise HTTPException(
            status_code=404,
            detail="Safe zone not found"
        )

    if zone_data.name is not None:
        safe_zone.name = zone_data.name

    if zone_data.latitude is not None:
        safe_zone.latitude = zone_data.latitude

    if zone_data.longitude is not None:
        safe_zone.longitude = zone_data.longitude

    if zone_data.radius_meters is not None:
        safe_zone.radius_meters = zone_data.radius_meters

    if zone_data.is_active is not None:
        safe_zone.is_active = zone_data.is_active

    db.commit()
    db.refresh(safe_zone)

    return safe_zone