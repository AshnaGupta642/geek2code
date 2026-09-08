from pydantic import BaseModel, Field


class AIVoiceRequest(BaseModel):
    patient_id: int = Field(gt=0)
    audio_url: str = Field(min_length=1, max_length=500)
    language: str = Field(
        default="en",
        min_length=2,
        max_length=10
    )
    conversation_id: str | None = Field(
        default=None,
        max_length=100
    )


class AIVoiceResponse(BaseModel):
    conversation_id: str

    transcript: str | None = None
    response_text: str | None = None
    response_audio_url: str | None = None

    detected_language: str
    intent: str | None = None