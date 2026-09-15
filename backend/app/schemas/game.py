from datetime import datetime

from pydantic import BaseModel, Field


class GameCreate(BaseModel):
    game_id: str = Field(
        min_length=1,
        max_length=20
    )

    name: str = Field(
        min_length=1,
        max_length=100
    )

    game_type: str = Field(
        min_length=1,
        max_length=50
    )

    difficulty: str = Field(
        default="easy",
        max_length=20
    )

    description: str | None = None

    offline_supported: bool = True


class GameResponse(BaseModel):
    id: int
    game_id: str
    name: str
    game_type: str
    difficulty: str
    description: str | None
    offline_supported: bool
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True