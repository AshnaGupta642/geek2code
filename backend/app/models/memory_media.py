from datetime import datetime, timezone

from sqlalchemy import ForeignKey, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class MemoryMedia(Base):
    __tablename__ = "memory_media"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    memory_id: Mapped[int] = mapped_column(
        ForeignKey("memories.id"),
        nullable=False,
        index=True
    )

    media_type: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    media_url: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    caption: Mapped[str | None] = mapped_column(
        String(300),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )