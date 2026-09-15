from datetime import datetime

from pydantic import BaseModel, Field


class FaceProfileCreate(BaseModel):
    family_member_id: int = Field(gt=0)
    face_image_url: str | None = None
    embedding_reference: str | None = None


class FaceProfileResponse(BaseModel):
    id: int
    patient_id: int
    family_member_id: int
    person_name: str
    face_image_url: str | None
    embedding_reference: str | None
    created_at: datetime

    class Config:
        from_attributes = True


class FaceRecognitionResult(BaseModel):
    family_member_id: int | None
    person_name: str | None
    confidence: float | None
    matched: bool