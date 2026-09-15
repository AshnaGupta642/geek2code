from datetime import date, datetime

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
    medicine_adherence: float
    missed_reminders: int
    games_completed: int
    average_game_accuracy: float
    cognitive_trend: str


class CaregiverPatientProfileUpdate(BaseModel):
    name: str
    email: str
    date_of_birth: date | None = None
    language: str
    address: str | None = None
    emergency_contact: str | None = None


class CaregiverPatientProfileResponse(BaseModel):
    patient_id: int
    user_id: int
    name: str
    email: str
    date_of_birth: date | None
    language: str
    address: str | None
    emergency_contact: str | None
    linked: bool
