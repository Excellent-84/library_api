from typing import Annotated

from annotated_types import MaxLen, MinLen
from pydantic import BaseModel, EmailStr

from .enums import UserRole


class UserBase(BaseModel):
    username: Annotated[str, MinLen(3), MaxLen(20)]
    email: EmailStr


class UserCreate(UserBase):
    password: str
    role: str = UserRole.READER.value


class UserResponse(UserBase):
    id: int
    is_active: bool
    role: str

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    username: str | None = None


class RoleUpdate(BaseModel):
    new_role: str
