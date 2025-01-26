from typing import Annotated, Optional

from annotated_types import MaxLen, MinLen
from pydantic import BaseModel, EmailStr

from .enums import UserRole


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    username: Annotated[str, MinLen(3), MaxLen(20)]
    password: Annotated[str, MinLen(8), MaxLen(16)]
    role: str = UserRole.READER.value


class UserUpdate(BaseModel):
    username: Optional[Annotated[str, MinLen(3), MaxLen(20)]] = None
    password: Optional[Annotated[str, MinLen(8), MaxLen(16)]] = None


class UserResponse(UserBase):
    id: int
    username: str
    is_active: bool
    role: str

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    email: EmailStr
    password: Annotated[str, MinLen(8), MaxLen(16)]


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class RoleUpdate(BaseModel):
    new_role: str
