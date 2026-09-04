from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models.activity_event import ActivityEvent
from app.models.alert import Alert
from app.models.reminder_history import ReminderHistory

from app.core.dependencies import get_current_caregiver
from app.database.database import get_db

from app.models.family_member import FamilyMember
from app.models.patient import Patient
from app.models.user import User
from app.models.game_result import GameResult
from app.schemas.caregiver import CaregiverPatientOverviewResponse


router = APIRouter(
    prefix="/api/caregiver",
    tags=["Caregiver"]
)


# --------------------------------------------------
# PATIENT OVERVIEW
# --------------------------------------------------

@router.get(
    "/patients/{patient_id}/overview",
    response_model=CaregiverPatientOverviewResponse
)
def get_patient_overview(
    patient_id: int,
    caregiver: FamilyMember = Depends(get_current_caregiver),
    db: Session = Depends(get_db)
):

    # --------------------------------------------------
    # CHECK CAREGIVER AUTHORIZATION
    # --------------------------------------------------

    if caregiver.patient_id != patient_id:
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to access this patient"
        )

    # --------------------------------------------------
    # GET PATIENT
    # --------------------------------------------------

    patient = db.query(Patient).filter(
        Patient.id == patient_id
    ).first()

    if patient is None:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    # --------------------------------------------------
    # GET PATIENT USER
    # --------------------------------------------------

    user = db.query(User).filter(
        User.id == patient.user_id
    ).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="Patient user not found"
        )

    # --------------------------------------------------
    # CALCULATE AGE
    # --------------------------------------------------

    age = None

    if patient.date_of_birth:

        from datetime import date

        today = date.today()

        age = today.year - patient.date_of_birth.year

        if (today.month, today.day) < (
            patient.date_of_birth.month,
            patient.date_of_birth.day
        ):
            age -= 1

    # --------------------------------------------------
    # LAST ACTIVE
    # --------------------------------------------------

    last_event = (
        db.query(ActivityEvent)
        .filter(
            ActivityEvent.patient_id == patient_id
        )
        .order_by(
            ActivityEvent.event_timestamp.desc()
        )
        .first()
    )

    last_active = (
        last_event.event_timestamp
        if last_event
        else None
    )

    # --------------------------------------------------
    # ACTIVE ALERTS
    # --------------------------------------------------

    alerts_count = (
        db.query(Alert)
        .filter(
            Alert.patient_id == patient_id,
            Alert.status == "ACTIVE"
        )
        .count()
    )

    # --------------------------------------------------
    # OVERALL STATUS
    # --------------------------------------------------

    if alerts_count > 0:
        overall_status = "ATTENTION"

    elif last_active is not None:
        overall_status = "ACTIVE"

    else:
        overall_status = "INACTIVE"

    # --------------------------------------------------
    # ORIENTATION STATUS
    # --------------------------------------------------

    orientation_event = (
        db.query(ActivityEvent)
        .filter(
            ActivityEvent.patient_id == patient_id,
            ActivityEvent.event_type == "ORIENTATION_COMPLETED"
        )
        .order_by(
            ActivityEvent.event_timestamp.desc()
        )
        .first()
    )

    if orientation_event:
        orientation_status = "GOOD"

    else:
        orientation_status = "UNKNOWN"
        # Cognitive engagement
    game_results = (
        db.query(GameResult)
        .filter(GameResult.patient_id == patient_id)
        .order_by(GameResult.completed_at.asc())
        .all()
    )

    games_completed = len(game_results)

    if games_completed > 0:
        average_game_accuracy = round(
            sum(result.accuracy for result in game_results) / games_completed,
            2
        )
    else:
        average_game_accuracy = 0

    if games_completed < 2:
        cognitive_trend = "INSUFFICIENT_DATA"
    else:
        first_accuracy = game_results[0].accuracy
        recent_accuracy = game_results[-1].accuracy
        change = recent_accuracy - first_accuracy

        if change >= 10:
            cognitive_trend = "IMPROVING"
        elif change <= -10:
            cognitive_trend = "DECLINING"
        else:
            cognitive_trend = "STABLE"
    # --------------------------------------------------
    # MEDICINE / REMINDER ADHERENCE
    # --------------------------------------------------

    reminder_history = (
        db.query(ReminderHistory)
        .filter(
            ReminderHistory.patient_id == patient_id
        )
        .all()
    )

    completed_reminders = sum(
        1
        for item in reminder_history
        if item.status == "COMPLETED"
    )

    missed_reminders = sum(
        1
        for item in reminder_history
        if item.status == "MISSED"
    )

    skipped_reminders = sum(
        1
        for item in reminder_history
        if item.status == "SKIPPED"
    )

    due_reminders = (
        completed_reminders
        + missed_reminders
        + skipped_reminders
    )

    if due_reminders > 0:

        medicine_adherence = round(
            (completed_reminders / due_reminders) * 100,
            2
        )

    else:

        medicine_adherence = 0

    # --------------------------------------------------
    # FINAL RESPONSE
    # --------------------------------------------------

    return {
        "patient_id": patient.id,
        "name": user.name,
        "age": age,
        "language": patient.language,
        "orientation_status": orientation_status,
        "last_active": last_active,
        "overall_status": overall_status,
        "alerts_count": alerts_count,

        "medicine_adherence": medicine_adherence,
        "missed_reminders": missed_reminders,
        "games_completed": games_completed,
        "average_game_accuracy": average_game_accuracy,
        "cognitive_trend": cognitive_trend
    }


# --------------------------------------------------
# PATIENT ACTIVITY
# --------------------------------------------------

@router.get(
    "/patients/{patient_id}/activity"
)
def get_patient_activity(
    patient_id: int,
    caregiver: FamilyMember = Depends(get_current_caregiver),
    db: Session = Depends(get_db)
):

    # Make sure caregiver belongs to patient
    if caregiver.patient_id != patient_id:
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to access this patient"
        )

    # Check patient exists
    patient = db.query(Patient).filter(
        Patient.id == patient_id
    ).first()

    if patient is None:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    # Get all activity events
    events = (
        db.query(ActivityEvent)
        .filter(
            ActivityEvent.patient_id == patient_id
        )
        .all()
    )

    # --------------------------------------------------
    # COUNT ACTIVITIES
    # --------------------------------------------------

    games_completed = sum(
        1
        for event in events
        if event.event_type == "GAME_COMPLETED"
    )

    memory_sessions = sum(
        1
        for event in events
        if event.event_type == "MEMORY_RECALL_COMPLETED"
    )

    voice_interactions = sum(
        1
        for event in events
        if event.event_type == "VOICE_COMMAND"
    )

    # --------------------------------------------------
    # DAILY PROGRESS
    # --------------------------------------------------

    daily_progress = {}

    for event in events:

        date_key = event.event_timestamp.date().isoformat()

        if date_key not in daily_progress:

            daily_progress[date_key] = {
                "date": date_key,
                "score": 0,
                "activities_completed": 0
            }

        if event.event_type in [
            "GAME_COMPLETED",
            "MEMORY_RECALL_COMPLETED",
            "ROUTINE_COMPLETED"
        ]:

            daily_progress[date_key][
                "activities_completed"
            ] += 1

    return {
        "patient_id": patient_id,
        "games_completed": games_completed,
        "average_score": None,
        "memory_sessions": memory_sessions,
        "voice_interactions": voice_interactions,

        "activity_summary": {
            "total_events": len(events)
        },

        "daily_progress": list(
            daily_progress.values()
        )
    }


# --------------------------------------------------
# TEST CAREGIVER AUTHENTICATION
# --------------------------------------------------

@router.get("/test")
def caregiver_test(
    caregiver: FamilyMember = Depends(get_current_caregiver)
):

    return {
        "success": True,
        "message": "Caregiver authorized successfully",
        "caregiver_id": caregiver.user_id,
        "patient_id": caregiver.patient_id,
        "family_member_id": caregiver.id
    }