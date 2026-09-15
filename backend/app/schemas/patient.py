from datetime import date
from pydantic import BaseModel


class PatientProfileCreate(BaseModel):
    date_of_birth: date | None = None
    language: str = "en"
    address: str | None = None
    emergency_contact: str | None = None


class PatientProfileResponse(BaseModel):
    id: int
    user_id: int
    name: str
    first_name: str
    date_of_birth: date | None
    language: str
    address: str | None
    emergency_contact: str | None

    class Config:
        from_attributes = True

class PatientProfileUpdate(BaseModel):
    date_of_birth: date | None = None
    language: str | None = None
    address: str | None = None
    emergency_contact: str | None = None