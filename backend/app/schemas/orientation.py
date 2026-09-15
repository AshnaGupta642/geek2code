from datetime import date, datetime

from pydantic import BaseModel


class OrientationResponse(BaseModel):
    patient_id: int
    current_date: date
    current_time: datetime
    day_of_week: str
    language: str
    location: str | None
    orientation_message: str
    status: str