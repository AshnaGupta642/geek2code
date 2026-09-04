from datetime import datetime

from pydantic import BaseModel, Field


class ReminderEventCreate(BaseModel):
    reminder_id: int
    status: str = Field(
        min_length=1,
        max_length=20
    )


class ReminderHistoryResponse(BaseModel):
    id: int
    reminder_id: int
    patient_id: int
    scheduled_at: datetime
    completed_at: datetime | None
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class ReminderAdherenceResponse(BaseModel):
    total: int
    completed: int
    missed: int
    skipped: int
    pending: int
    adherence_percentage: float