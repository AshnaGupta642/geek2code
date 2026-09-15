from datetime import datetime, timezone

from sqlalchemy import ForeignKey, String, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class FaceProfile(Base):
    __tablename__ = "face_profiles"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    patient_id: Mapped[int] = mapped_column(
        ForeignKey("patients.id"),
        nullable=False,
        index=True
    )

    family_member_id: Mapped[int] = mapped_column(
        ForeignKey("family_members.id"),
        nullable=False,
        index=True
    )

    person_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    face_image_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )

    embedding_reference: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )