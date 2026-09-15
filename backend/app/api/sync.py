import json
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.models.patient import Patient
from app.models.user import User
from app.models.sync_event import SyncEvent
from app.models.reminder import Reminder
from app.models.memory import Memory
from app.models.family_member import FamilyMember

from app.schemas.sync import (
    SyncRequest,
    SyncResponse
)

from app.core.dependencies import get_current_user


router = APIRouter(
    prefix="/api/sync",
    tags=["Sync"]
)


# --------------------------------------------------
# SYNC OFFLINE EVENTS
# --------------------------------------------------

@router.post(
    "/",
    response_model=SyncResponse
)
def sync_events(
    sync_data: SyncRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    # --------------------------------------------------
    # FIND PATIENT
    # --------------------------------------------------

    patient = (
        db.query(Patient)
        .filter(Patient.user_id == current_user.id)
        .first()
    )

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient profile not found"
        )

    # --------------------------------------------------
    # AUTHORIZATION
    # --------------------------------------------------

    if patient.id != sync_data.patient_id:
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to sync this patient's data"
        )

    synced_events = 0
    failed_events = []

    # --------------------------------------------------
    # PROCESS OFFLINE EVENTS
    # --------------------------------------------------

    for event in sync_data.events:

        try:

            # --------------------------------------------------
            # CHECK DUPLICATE EVENT
            # --------------------------------------------------

            existing_event = (
                db.query(SyncEvent)
                .filter(
                    SyncEvent.event_id == event.event_id,
                    SyncEvent.patient_id == patient.id,
                    SyncEvent.device_id == sync_data.device_id
                )
                .first()
            )

            # --------------------------------------------------
            # DUPLICATE EVENT
            # --------------------------------------------------

            if existing_event:
                synced_events += 1
                continue

            # --------------------------------------------------
            # CREATE SYNC EVENT
            # --------------------------------------------------

            sync_event = SyncEvent(
                patient_id=patient.id,
                device_id=sync_data.device_id,
                event_id=event.event_id,
                event_type=event.event_type,
                event_data=(
                    json.dumps(event.data)
                    if event.data is not None
                    else None
                ),
                event_timestamp=event.timestamp
            )

            db.add(sync_event)

            synced_events += 1

        except Exception:
            failed_events.append(event.event_id)

    # --------------------------------------------------
    # SAVE EVENTS
    # --------------------------------------------------

    try:
        db.commit()

    except Exception:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Failed to save offline sync events"
        )

    # --------------------------------------------------
    # SERVER UPDATES
    #
    # Send current server-side data back to the patient
    # so the offline device can update its local database.
    # --------------------------------------------------

    reminders = (
        db.query(Reminder)
        .filter(
            Reminder.patient_id == patient.id
        )
        .all()
    )

    memories = (
        db.query(Memory)
        .filter(
            Memory.patient_id == patient.id
        )
        .all()
    )

    family_members = (
        db.query(FamilyMember)
        .filter(
            FamilyMember.patient_id == patient.id,
            FamilyMember.is_active == True
        )
        .all()
    )

    # --------------------------------------------------
    # CONVERT REMINDERS
    # --------------------------------------------------

    reminder_updates = []

    for reminder in reminders:

        reminder_updates.append({
            "id": reminder.id,
            "patient_id": reminder.patient_id,
            "medicine_id": reminder.medicine_id,
            "voice_recording_id": reminder.voice_recording_id,
            "reminder_type": reminder.reminder_type,
            "reminder_text": reminder.reminder_text,
            "scheduled_time": (
                reminder.scheduled_time.isoformat()
                if reminder.scheduled_time
                else None
            ),
            "repeat_pattern": reminder.repeat_pattern,
            "status": reminder.status,
            "created_at": (
                reminder.created_at.isoformat()
                if reminder.created_at
                else None
            ),
            "updated_at": (
                reminder.updated_at.isoformat()
                if reminder.updated_at
                else None
            )
        })

    # --------------------------------------------------
    # CONVERT MEMORIES
    # --------------------------------------------------

    memory_updates = []

    for memory in memories:

        memory_updates.append({
            "id": memory.id,
            "patient_id": memory.patient_id,
            "title": memory.title,
            "story_text": memory.story_text,
            "summary": memory.summary,
            "memory_type": memory.memory_type,
            "tags": memory.tags,
            "people": memory.people,
            "event_date": (
                memory.event_date.isoformat()
                if memory.event_date
                else None
            ),
            "location": memory.location,
            "cover_photo_url": memory.cover_photo_url,
            "audio_url": memory.audio_url,
            "is_private": memory.is_private,
            "is_approved": memory.is_approved,
            "created_at": (
                memory.created_at.isoformat()
                if memory.created_at
                else None
            ),
            "updated_at": (
                memory.updated_at.isoformat()
                if memory.updated_at
                else None
            )
        })

    # --------------------------------------------------
    # CONVERT FAMILY MEMBERS
    # --------------------------------------------------

    family_updates = []

    for family_member in family_members:

        family_updates.append({
            "id": family_member.id,
            "patient_id": family_member.patient_id,
            "user_id": family_member.user_id,
            "name": family_member.name,
            "relationship": family_member.relationship,
            "phone": family_member.phone,
            "photo_url": family_member.photo_url,
            "is_caregiver": family_member.is_caregiver,
            "is_active": family_member.is_active,
            "created_at": (
                family_member.created_at.isoformat()
                if family_member.created_at
                else None
            )
        })

    # --------------------------------------------------
    # SERVER UPDATES
    # --------------------------------------------------

    server_updates = {
        "reminders": reminder_updates,
        "memories": memory_updates,
        "family": family_updates
    }

    # --------------------------------------------------
    # NEXT SYNC TOKEN
    # --------------------------------------------------

    next_sync_token = datetime.now(timezone.utc).isoformat()

    # --------------------------------------------------
    # RESPONSE
    # --------------------------------------------------

    return {
        "success": len(failed_events) == 0,
        "synced_events": synced_events,
        "failed_events": failed_events,
        "server_updates": server_updates,
        "next_sync_token": next_sync_token
    }