from datetime import datetime, timezone

from sqlalchemy import String, Text, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func
from app.database.base import Base


class Game(Base):

    __tablename__ = "games"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    game_id: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False,
        index=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    game_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    difficulty: Mapped[str] = mapped_column(
        String(20),
        default="easy",
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    offline_supported: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )