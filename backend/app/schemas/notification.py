from datetime import datetime
from pydantic import BaseModel


class NotificationResponse(BaseModel):
    id: int
    user_id: int
    patient_id: int | None
    notification_type: str
    title: str
    message: str
    is_read: bool
    created_at: datetime
    read_at: datetime | None

    class Config:
        from_attributes = True