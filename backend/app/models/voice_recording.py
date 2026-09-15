from datetime import datetime, timezone

from sqlalchemy import ForeignKey, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class VoiceRecording(Base):
    __tablename__ = "voice_recordings"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    patient_id: Mapped[int] = mapped_column(
        ForeignKey("patients.id"),
        nullable=False,
        index=True
    )

    family_member_id: Mapped[int | None] = mapped_column(
        ForeignKey("family_members.id"),
        nullable=True,
        index=True
    )

    memory_id: Mapped[int | None] = mapped_column(
        ForeignKey("memories.id"),
        nullable=True,
        index=True
    )

    audio_url: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    language: Mapped[str] = mapped_column(
        String(10),
        default="en",
        nullable=False
    )

    recording_type: Mapped[str] = mapped_column(
        String(30),
        nullable=False
    )

    duration_seconds: Mapped[int | None] = mapped_column(
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )