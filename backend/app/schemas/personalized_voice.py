from pydantic import BaseModel, Field


class PersonalizedVoiceRequest(BaseModel):
    patient_id: int = Field(gt=0)
    caregiver_id: int = Field(gt=0)
    audio_url: str = Field(min_length=1, max_length=500)
    reminder_type: str = Field(min_length=1, max_length=50)
    reminder_text: str = Field(min_length=1, max_length=500)


class PersonalizedVoiceResponse(BaseModel):
    voice_recording_id: str
    patient_id: int
    caregiver_id: int
    audio_url: str
    duration_seconds: int | None = None
    status: str