from pydantic import BaseModel, EmailStr, Field
from app.schemas.game_session import GameStartRequest, GameStartResponse
from app.schemas.game_result import GameResultCreate, GameResultResponse

class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=6, max_length=72)
    role: str


class RegisterResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str