from datetime import datetime, timezone

from sqlalchemy import ForeignKey, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class EmergencyEvent(Base):

    __tablename__ = "emergency_events"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    patient_id: Mapped[int] = mapped_column(
        ForeignKey("patients.id"),
        nullable=False,
        index=True
    )

    trigger: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    latitude: Mapped[float | None] = mapped_column(
        nullable=True
    )

    longitude: Mapped[float | None] = mapped_column(
        nullable=True
    )

    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(30),
        default="ALERT_SENT",
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )