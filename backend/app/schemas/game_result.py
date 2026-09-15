from datetime import datetime

from pydantic import BaseModel, Field


class GameResultCreate(BaseModel):
    session_id: str = Field(min_length=1, max_length=100)
    score: float = Field(ge=0)
    accuracy: float = Field(ge=0, le=100)
    mistakes: int = Field(default=0, ge=0)
    duration_seconds: int = Field(gt=0)
    attempts: int = Field(default=1, ge=1)
    hints_used: int = Field(default=0, ge=0)
    response_time: float | None = Field(default=None, ge=0)
    completed_at: datetime


class GameResultResponse(BaseModel):
    success: bool
    session_id: str
    game_id: str
    score: float
    accuracy: float
    next_difficulty: str