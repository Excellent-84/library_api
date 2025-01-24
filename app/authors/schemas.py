from datetime import date
from typing import Optional

from pydantic import BaseModel


class AuthorBase(BaseModel):
    name: str
    birth_date: date


class AuthorCreate(AuthorBase):
    biography: Optional[str] = None


class AuthorUpdate(BaseModel):
    name: Optional[str]
    biography: Optional[str]
    birth_date: Optional[date]


class AuthorRead(AuthorBase):
    id: int

    class Config:
        from_attributes = True
