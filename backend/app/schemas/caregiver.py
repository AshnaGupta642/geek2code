from datetime import datetime
from pydantic import BaseModel


class CaregiverPatientOverviewResponse(BaseModel):
    patient_id: int
    name: str
    age: int | None
    language: str
    orientation_status: str
    last_active: datetime | None
    overall_status: str
    alerts_count: int

    # Reminder / medicine adherence
    medicine_adherence: float
    missed_reminders: int
    games_completed: int
    average_game_accuracy: float
    cognitive_trend: str