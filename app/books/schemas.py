from datetime import date
from typing import Annotated, List, Optional

from annotated_types import MaxLen, MinLen
from pydantic import BaseModel, ConfigDict, Field, field_validator


class BookBase(BaseModel):
    title: Annotated[str, MinLen(3), MaxLen(100)]
    description: Optional[Annotated[str, MaxLen(1000)]] = None
    publication_date: date
    genre: Annotated[str, MinLen(3), MaxLen(50)]
    available_copies: int = Field(..., ge=0)


class BookCreate(BookBase):
    author_ids: List[int]


class BookResponse(BookBase):
    id: int
    authors: List[str]

    model_config = ConfigDict(from_attributes=True)

    @field_validator("authors", mode="before")
    def convert_authors(cls, value):  # noqa
        return [author.name for author in value]
