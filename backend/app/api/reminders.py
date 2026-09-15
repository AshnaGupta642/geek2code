from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.reminder import Reminder
from app.models.patient import Patient
from app.models.medicine import Medicine
from app.models.user import User

from app.schemas.reminder import (
    ReminderCreate,
    ReminderUpdate,
    ReminderResponse
)

from app.core.dependencies import get_current_user
from app.models.family_member import FamilyMember
from app.core.dependencies import get_current_caregiver
from app.models.voice_recording import VoiceRecording


router = APIRouter(
    prefix="/api/reminders",
    tags=["Reminders"]
)


# --------------------------------------------------
# CREATE REMINDER
# --------------------------------------------------

@router.post(
    "/",
    response_model=ReminderResponse
)
def create_reminder(
    reminder_data: ReminderCreate,
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

    # If medicine_id is provided,
    # make sure it belongs to this patient.
    if reminder_data.medicine_id is not None:

        medicine = db.query(Medicine).filter(
            Medicine.id == reminder_data.medicine_id,
            Medicine.patient_id == patient.id,
            Medicine.is_active == True
        ).first()

        if not medicine:
            raise HTTPException(
                status_code=404,
                detail="Medicine not found"
            )
    # Validate voice recording if provided
    if reminder_data.voice_recording_id is not None:

        voice_recording = db.query(VoiceRecording).filter(
            VoiceRecording.id == reminder_data.voice_recording_id,
            VoiceRecording.patient_id == patient.id
        ).first()

        if not voice_recording:
            raise HTTPException(
                status_code=404,
                detail="Voice recording not found for this patient"
            )
    reminder = Reminder(
        patient_id=patient.id,
        medicine_id=reminder_data.medicine_id,
        reminder_type=reminder_data.reminder_type,
        reminder_text=reminder_data.reminder_text,
        scheduled_time=reminder_data.scheduled_time,
        repeat_pattern=reminder_data.repeat_pattern,
        voice_recording_id=reminder_data.voice_recording_id,
        status="ACTIVE"
    )

    db.add(reminder)
    db.commit()
    db.refresh(reminder)

    return reminder


# --------------------------------------------------
# GET ALL REMINDERS
# --------------------------------------------------

@router.get(
    "/",
    response_model=list[ReminderResponse]
)
def get_reminders(
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

    reminders = db.query(Reminder).filter(
        Reminder.patient_id == patient.id
    ).order_by(
        Reminder.scheduled_time.asc()
    ).all()

    return reminders


# --------------------------------------------------
# GET SINGLE REMINDER
# --------------------------------------------------

@router.get(
    "/{reminder_id}",
    response_model=ReminderResponse
)
def get_reminder(
    reminder_id: int,
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

    reminder = db.query(Reminder).filter(
        Reminder.id == reminder_id,
        Reminder.patient_id == patient.id
    ).first()

    if not reminder:
        raise HTTPException(
            status_code=404,
            detail="Reminder not found"
        )

    return reminder


# --------------------------------------------------
# UPDATE REMINDER
# --------------------------------------------------

@router.put(
    "/{reminder_id}",
    response_model=ReminderResponse
)
def update_reminder(
    reminder_id: int,
    reminder_data: ReminderUpdate,
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

    reminder = db.query(Reminder).filter(
        Reminder.id == reminder_id,
        Reminder.patient_id == patient.id
    ).first()

    if not reminder:
        raise HTTPException(
            status_code=404,
            detail="Reminder not found"
        )

    # If medicine is being changed,
    # verify it belongs to this patient.
    if reminder_data.medicine_id is not None:

        medicine = db.query(Medicine).filter(
            Medicine.id == reminder_data.medicine_id,
            Medicine.patient_id == patient.id,
            Medicine.is_active == True
        ).first()

        if not medicine:
            raise HTTPException(
                status_code=404,
                detail="Medicine not found"
            )

        reminder.medicine_id = reminder_data.medicine_id
    # If voice recording is being changed,
    # verify that it belongs to this patient.
    if reminder_data.voice_recording_id is not None:

        voice_recording = db.query(VoiceRecording).filter(
            VoiceRecording.id == reminder_data.voice_recording_id,
            VoiceRecording.patient_id == patient.id
        ).first()

        if not voice_recording:
            raise HTTPException(
                status_code=404,
                detail="Voice recording not found for this patient"
            )

        reminder.voice_recording_id = reminder_data.voice_recording_id
    if reminder_data.reminder_type is not None:
        reminder.reminder_type = reminder_data.reminder_type

    if reminder_data.reminder_text is not None:
        reminder.reminder_text = reminder_data.reminder_text

    if reminder_data.scheduled_time is not None:
        reminder.scheduled_time = reminder_data.scheduled_time

    if reminder_data.repeat_pattern is not None:
        reminder.repeat_pattern = reminder_data.repeat_pattern

    if reminder_data.status is not None:

        if reminder_data.status not in [
            "ACTIVE",
            "PAUSED"
        ]:
            raise HTTPException(
                status_code=400,
                detail="Status must be ACTIVE or PAUSED"
            )

        reminder.status = reminder_data.status

    db.commit()
    db.refresh(reminder)

    return reminder


# --------------------------------------------------
# DELETE REMINDER
# --------------------------------------------------

@router.delete(
    "/{reminder_id}"
)
def delete_reminder(
    reminder_id: int,
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

    reminder = db.query(Reminder).filter(
        Reminder.id == reminder_id,
        Reminder.patient_id == patient.id
    ).first()

    if not reminder:
        raise HTTPException(
            status_code=404,
            detail="Reminder not found"
        )

    # Soft delete
    reminder.status = "PAUSED"

    db.commit()

    return {
        "success": True,
        "message": "Reminder removed successfully"
    }

# --------------------------------------------------
# CAREGIVER CREATE REMINDER
# --------------------------------------------------

@router.post(
    "/caregiver/{patient_id}"
)
def caregiver_create_reminder(
    patient_id: int,
    reminder_data: ReminderCreate,
    caregiver: FamilyMember = Depends(get_current_caregiver),
    db: Session = Depends(get_db)
):

    # Make sure caregiver belongs to this patient
    if caregiver.patient_id != patient_id:
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to manage this patient's reminders"
        )

    # If medicine_id is provided, verify it belongs to this patient
    if reminder_data.medicine_id is not None:

        medicine = db.query(Medicine).filter(
            Medicine.id == reminder_data.medicine_id,
            Medicine.patient_id == patient_id,
            Medicine.is_active == True
        ).first()

        if not medicine:
            raise HTTPException(
                status_code=404,
                detail="Medicine not found"
            )
    # Validate voice recording if provided
    if reminder_data.voice_recording_id is not None:

        voice_recording = db.query(VoiceRecording).filter(
            VoiceRecording.id == reminder_data.voice_recording_id,
            VoiceRecording.patient_id == patient_id,
            VoiceRecording.family_member_id == caregiver.id
        ).first()

        if not voice_recording:
            raise HTTPException(
                status_code=404,
                detail="Voice recording not found for this caregiver and patient"
            )
    reminder = Reminder(
        patient_id=patient_id,
        medicine_id=reminder_data.medicine_id,
        reminder_type=reminder_data.reminder_type,
        reminder_text=reminder_data.reminder_text,
        scheduled_time=reminder_data.scheduled_time,
        repeat_pattern=reminder_data.repeat_pattern,
        voice_recording_id=reminder_data.voice_recording_id,
        status="ACTIVE"
    )

    db.add(reminder)
    db.commit()
    db.refresh(reminder)

    return {
        "reminder_id": reminder.id,
        "patient_id": patient_id,
        "caregiver_id": caregiver.id,
        "status": "created"
    }
# --------------------------------------------------
# CAREGIVER UPDATE REMINDER
# --------------------------------------------------

@router.put(
    "/caregiver/{patient_id}/{reminder_id}"
)
def caregiver_update_reminder(
    patient_id: int,
    reminder_id: int,
    reminder_data: ReminderUpdate,
    caregiver: FamilyMember = Depends(get_current_caregiver),
    db: Session = Depends(get_db)
):

    # Make sure caregiver belongs to this patient
    if caregiver.patient_id != patient_id:
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to manage this patient's reminders"
        )

    reminder = db.query(Reminder).filter(
        Reminder.id == reminder_id,
        Reminder.patient_id == patient_id
    ).first()

    if not reminder:
        raise HTTPException(
            status_code=404,
            detail="Reminder not found"
        )

    # Update scheduled time
    if reminder_data.scheduled_time is not None:
        reminder.scheduled_time = reminder_data.scheduled_time

    # Update status
    if reminder_data.status is not None:

        if reminder_data.status not in [
            "ACTIVE",
            "PAUSED"
        ]:
            raise HTTPException(
                status_code=400,
                detail="Status must be ACTIVE or PAUSED"
            )

        reminder.status = reminder_data.status

    # Optional fields
        # Update voice recording
    if reminder_data.voice_recording_id is not None:

        voice_recording = db.query(VoiceRecording).filter(
            VoiceRecording.id == reminder_data.voice_recording_id,
            VoiceRecording.patient_id == patient_id,
            VoiceRecording.family_member_id == caregiver.id
        ).first()

        if not voice_recording:
            raise HTTPException(
                status_code=404,
                detail="Voice recording not found for this caregiver and patient"
            )

        reminder.voice_recording_id = reminder_data.voice_recording_id
    if reminder_data.reminder_type is not None:
        reminder.reminder_type = reminder_data.reminder_type

    if reminder_data.reminder_text is not None:
        reminder.reminder_text = reminder_data.reminder_text

    if reminder_data.repeat_pattern is not None:
        reminder.repeat_pattern = reminder_data.repeat_pattern

    db.commit()
    db.refresh(reminder)

    return {
        "reminder_id": reminder.id,
        "patient_id": patient_id,
        "status": "updated"
    }
# --------------------------------------------------
# CAREGIVER GET PATIENT REMINDERS
# --------------------------------------------------

@router.get(
    "/caregiver/{patient_id}",
    response_model=list[ReminderResponse]
)
def caregiver_get_reminders(
    patient_id: int,
    caregiver: FamilyMember = Depends(get_current_caregiver),
    db: Session = Depends(get_db)
):

    # Make sure caregiver belongs to this patient
    if caregiver.patient_id != patient_id:
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to view this patient's reminders"
        )

    reminders = (
        db.query(Reminder)
        .filter(
            Reminder.patient_id == patient_id
        )
        .order_by(Reminder.scheduled_time.asc())
        .all()
    )

    return reminders