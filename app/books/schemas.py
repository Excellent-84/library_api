from datetime import date
from typing import List

from pydantic import BaseModel, Field


class BookBase(BaseModel):
    title: str = Field(..., max_length=100)
    description: str | None = Field(None, max_length=1000)
    publication_date: date
    genre: str = Field(..., max_length=50)
    available_copies: int = Field(..., ge=0)


class BookCreate(BookBase):
    author_ids: List[int]


class BookResponse(BookBase):
    id: int
    authors: List[str]

    class Config:
        from_attributes = True
