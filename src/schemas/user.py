from pydantic import BaseModel, EmailStr
from src.models.user import UserRole


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: UserRole = UserRole.CLIENT  # За замовчуванням звичайний клієнт


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    role: UserRole
    is_active: bool

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None
    role: str | None = None