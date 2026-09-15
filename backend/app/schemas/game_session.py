from datetime import datetime

from pydantic import BaseModel, Field


class GameStartRequest(BaseModel):
    game_id: str = Field(min_length=1, max_length=20)


class GameStartResponse(BaseModel):
    session_id: str
    game_id: str
    difficulty: str
    game_data: dict
    started_at: datetime