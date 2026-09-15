from datetime import datetime

from pydantic import BaseModel, Field


class LocationCreate(BaseModel):
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    accuracy_meters: float | None = Field(
        default=None,
        ge=0
    )
    timestamp: datetime


class LocationResponse(BaseModel):
    id: int
    patient_id: int
    latitude: float
    longitude: float
    accuracy_meters: float | None
    timestamp: datetime

    class Config:
        from_attributes = True