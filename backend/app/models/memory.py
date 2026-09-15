from datetime import date, datetime, timezone

from sqlalchemy import ForeignKey, String, Text, DateTime, Date, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Memory(Base):
    __tablename__ = "memories"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    patient_id: Mapped[int] = mapped_column(
        ForeignKey("patients.id"),
        nullable=False,
        index=True
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    story_text: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    summary: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    memory_type: Mapped[str] = mapped_column(
        String(50),
        default="general",
        nullable=False,
        index=True
    )

    tags: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    people: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    event_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True
    )

    location: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True
    )

    cover_photo_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )

    audio_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )

    is_private: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    is_approved: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )