from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


def _blank_to_none(value):
    if isinstance(value, str) and not value.strip():
        return None
    return value


def _normalize_event_date(value):
    value = _blank_to_none(value)
    if isinstance(value, str) and "T" in value:
        return value.split("T", 1)[0]
    return value


class MemoryCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    story_text: str | None = None
    summary: str | None = None

    memory_type: str = Field(
        default="general",
        max_length=50
    )

    tags: str | None = None
    people: str | None = None
    event_date: date | None = None
    location: str | None = Field(
        default=None,
        max_length=200
    )

    cover_photo_url: str | None = Field(
        default=None,
        max_length=500
    )

    audio_url: str | None = Field(
        default=None,
        max_length=500
    )

    is_private: bool = False
    is_approved: bool = False

    @field_validator(
        "story_text", "summary", "tags", "people", "location",
        "cover_photo_url", "audio_url",
        mode="before",
    )
    @classmethod
    def empty_optional(cls, value):
        return _blank_to_none(value)

    @field_validator("event_date", mode="before")
    @classmethod
    def empty_event_date(cls, value):
        return _normalize_event_date(value)


class MemoryUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=200
    )

    story_text: str | None = None
    summary: str | None = None

    memory_type: str | None = Field(
        default=None,
        max_length=50
    )

    tags: str | None = None
    people: str | None = None
    event_date: date | None = None

    location: str | None = Field(
        default=None,
        max_length=200
    )

    cover_photo_url: str | None = Field(
        default=None,
        max_length=500
    )

    audio_url: str | None = Field(
        default=None,
        max_length=500
    )

    is_private: bool | None = None
    is_approved: bool | None = None

    @field_validator(
        "story_text", "summary", "tags", "people", "location",
        "cover_photo_url", "audio_url", "title", "memory_type",
        mode="before",
    )
    @classmethod
    def empty_optional(cls, value):
        return _blank_to_none(value)

    @field_validator("event_date", mode="before")
    @classmethod
    def empty_event_date(cls, value):
        return _normalize_event_date(value)


class MemoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    patient_id: int

    title: str
    story_text: str | None
    summary: str | None

    memory_type: str
    tags: str | None
    people: str | None
    event_date: date | None
    location: str | None

    cover_photo_url: str | None
    audio_url: str | None

    is_private: bool
    is_approved: bool

    created_at: datetime
    updated_at: datetime
