from datetime import datetime

from pydantic import BaseModel, Field


class ActivityEventCreate(BaseModel):
    event_type: str = Field(
        min_length=1,
        max_length=50
    )

    event_data: str | None = None

    event_timestamp: datetime


class ActivityEventResponse(BaseModel):
    id: int
    patient_id: int
    event_type: str
    event_data: str | None
    event_timestamp: datetime
    created_at: datetime

    class Config:
        from_attributes = True