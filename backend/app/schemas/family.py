from datetime import datetime

from pydantic import BaseModel


class FamilyMemberCreate(BaseModel):
    name: str
    relationship: str
    phone: str | None = None
    photo_url: str | None = None
    is_caregiver: bool = False
    user_id: int | None = None


class FamilyMemberUpdate(BaseModel):
    name: str | None = None
    relationship: str | None = None
    phone: str | None = None
    photo_url: str | None = None
    is_caregiver: bool | None = None
    is_active: bool | None = None
    user_id: int | None = None


class FamilyMemberResponse(BaseModel):
    id: int
    patient_id: int
    user_id: int | None
    name: str
    relationship: str
    phone: str | None
    photo_url: str | None
    is_caregiver: bool
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True