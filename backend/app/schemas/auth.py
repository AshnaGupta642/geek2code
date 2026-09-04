from pydantic import BaseModel, EmailStr, Field


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

class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=72)


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    role: str