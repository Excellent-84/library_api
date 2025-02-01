from datetime import date
from typing import Annotated, Optional

from annotated_types import MaxLen, MinLen
from pydantic import BaseModel, ConfigDict


class AuthorBase(BaseModel):
    name: Annotated[str, MinLen(3), MaxLen(50)]
    birth_date: date
    biography: Optional[Annotated[str, MaxLen(1000)]] = None


class AuthorCreate(AuthorBase):
    pass


class AuthorUpdate(BaseModel):
    name: Optional[Annotated[str, MinLen(3), MaxLen(50)]] = None
    birth_date: Optional[date] = None
    biography: Optional[Annotated[str, MaxLen(1000)]] = None


class AuthorRead(AuthorBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
