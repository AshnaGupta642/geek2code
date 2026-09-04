from datetime import datetime, timezone

from sqlalchemy import ForeignKey, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class MemoryRelationship(Base):
    __tablename__ = "memory_relationships"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    memory_id: Mapped[int] = mapped_column(
        ForeignKey("memories.id"),
        nullable=False,
        index=True
    )

    source_element_id: Mapped[int] = mapped_column(
        ForeignKey("memory_elements.id"),
        nullable=False
    )

    target_element_id: Mapped[int] = mapped_column(
        ForeignKey("memory_elements.id"),
        nullable=False
    )

    relationship_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )