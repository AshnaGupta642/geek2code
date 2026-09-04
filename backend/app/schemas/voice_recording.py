from datetime import datetime

from pydantic import BaseModel, Field


class VoiceRecordingCreate(BaseModel):
    memory_id: int | None = None
    family_member_id: int | None = None

    audio_url: str = Field(min_length=1, max_length=500)

    language: str = Field(
        default="en",
        min_length=2,
        max_length=10
    )

    recording_type: str = Field(
        min_length=1,
        max_length=30
    )

    duration_seconds: int | None = Field(
        default=None,
        ge=0
    )


class VoiceRecordingResponse(BaseModel):
    id: int
    patient_id: int
    family_member_id: int | None
    memory_id: int | None
    audio_url: str
    language: str
    recording_type: str
    duration_seconds: int | None
    created_at: datetime

    class Config:
        from_attributes = True