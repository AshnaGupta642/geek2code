from datetime import datetime, time

from pydantic import BaseModel, Field


class ReminderCreate(BaseModel):
    medicine_id: int | None = None

    voice_recording_id: int | None = None

    reminder_type: str = Field(
        min_length=1,
        max_length=30
    )

    reminder_text: str = Field(
        min_length=1,
        max_length=500
    )

    scheduled_time: time

    repeat_pattern: str = Field(
        default="DAILY",
        max_length=30
    )


class ReminderUpdate(BaseModel):
    medicine_id: int | None = None

    voice_recording_id: int | None = None

    reminder_type: str | None = Field(
        default=None,
        min_length=1,
        max_length=30
    )

    reminder_text: str | None = Field(
        default=None,
        min_length=1,
        max_length=500
    )

    scheduled_time: time | None = None

    repeat_pattern: str | None = Field(
        default=None,
        max_length=30
    )

    status: str | None = Field(
        default=None,
        max_length=20
    )


class ReminderResponse(BaseModel):
    id: int
    patient_id: int
    medicine_id: int | None
    voice_recording_id: int | None
    reminder_type: str
    reminder_text: str
    scheduled_time: time
    repeat_pattern: str
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True