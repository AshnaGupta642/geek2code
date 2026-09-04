from datetime import date, datetime

from pydantic import BaseModel, Field


class MedicineCreate(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    dosage: str | None = Field(default=None, max_length=100)
    instructions: str | None = None
    start_date: date | None = None
    end_date: date | None = None


class MedicineUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=150)
    dosage: str | None = Field(default=None, max_length=100)
    instructions: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    is_active: bool | None = None


class MedicineResponse(BaseModel):
    id: int
    patient_id: int
    name: str
    dosage: str | None
    instructions: str | None
    start_date: date | None
    end_date: date | None
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True