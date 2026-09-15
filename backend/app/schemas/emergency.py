from datetime import datetime

from pydantic import BaseModel, Field


class EmergencyCreate(BaseModel):
    trigger: str = Field(
        min_length=1,
        max_length=50
    )

    latitude: float | None = Field(
        default=None,
        ge=-90,
        le=90
    )

    longitude: float | None = Field(
        default=None,
        ge=-180,
        le=180
    )

    timestamp: datetime


class EmergencyResponse(BaseModel):
    success: bool
    event_id: int
    status: str
    caregiver_notified: bool