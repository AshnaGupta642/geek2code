from datetime import datetime, timezone

from sqlalchemy import ForeignKey, String, DateTime, Float, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class GameResult(Base):
    __tablename__ = "game_results"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    session_id: Mapped[str] = mapped_column(
        ForeignKey("game_sessions.session_id"),
        nullable=False,
        index=True
    )

    patient_id: Mapped[int] = mapped_column(
        ForeignKey("patients.id"),
        nullable=False,
        index=True
    )

    game_id: Mapped[str] = mapped_column(
        ForeignKey("games.game_id"),
        nullable=False,
        index=True
    )

    score: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    accuracy: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    mistakes: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )

    duration_seconds: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    attempts: Mapped[int] = mapped_column(
        Integer,
        default=1,
        nullable=False
    )

    hints_used: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )

    response_time: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    difficulty: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    completed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )