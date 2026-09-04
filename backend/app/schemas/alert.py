from datetime import datetime

from pydantic import BaseModel, Field


class AlertCreate(BaseModel):
    alert_type: str = Field(
        min_length=1,
        max_length=50
    )

    message: str = Field(
        min_length=1
    )

    severity: str = Field(
        default="MEDIUM",
        max_length=20
    )


class AlertResponse(BaseModel):
    id: int
    patient_id: int
    alert_type: str
    message: str
    severity: str
    status: str
    created_at: datetime
    resolved_at: datetime | None

    class Config:
        from_attributes = True