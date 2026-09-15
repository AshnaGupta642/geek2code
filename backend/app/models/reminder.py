from datetime import datetime, time, timezone

from sqlalchemy import ForeignKey, String, DateTime, Time
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Reminder(Base):
    __tablename__ = "reminders"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    patient_id: Mapped[int] = mapped_column(
        ForeignKey("patients.id"),
        nullable=False,
        index=True
    )

    # Optional link to a medicine.
    # A reminder can also be for things like water,
    # exercise, appointments, etc.
    medicine_id: Mapped[int | None] = mapped_column(
        ForeignKey("medicines.id"),
        nullable=True,
        index=True
    )
    voice_recording_id: Mapped[int | None] = mapped_column(
    ForeignKey("voice_recordings.id"),
    nullable=True,
    index=True
)

    reminder_type: Mapped[str] = mapped_column(
        String(30),
        nullable=False
    )

    reminder_text: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    scheduled_time: Mapped[time] = mapped_column(
        Time,
        nullable=False
    )

    repeat_pattern: Mapped[str] = mapped_column(
        String(30),
        default="DAILY",
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="ACTIVE",
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