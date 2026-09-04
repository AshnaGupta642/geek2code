from datetime import datetime, timezone

from sqlalchemy import ForeignKey, String, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class MemoryElement(Base):
    __tablename__ = "memory_elements"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    memory_id: Mapped[int] = mapped_column(
        ForeignKey("memories.id"),
        nullable=False,
        index=True
    )

    element_type: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    label: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )