from datetime import datetime

from pydantic import BaseModel, Field


class SyncEventData(BaseModel):
    event_id: str = Field(
        min_length=1,
        max_length=100
    )

    event_type: str = Field(
        min_length=1,
        max_length=50
    )

    timestamp: datetime

    data: dict | None = None


class SyncRequest(BaseModel):
    patient_id: int

    device_id: str = Field(
        min_length=1,
        max_length=100
    )

    last_sync_at: datetime | None = None

    events: list[SyncEventData] = []


class SyncResponse(BaseModel):
    success: bool
    synced_events: int
    failed_events: list[str]
    server_updates: dict
    next_sync_token: str