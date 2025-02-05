"""
Pydantic-схемы для работы с книгами:

- Валидация данных книг (создание, обновление).
- Формирование ответов API с информацией о книгах.
"""

from datetime import date
from typing import Annotated, List, Optional

from annotated_types import MaxLen, MinLen
from pydantic import BaseModel, ConfigDict, Field, field_validator


class BookBase(BaseModel):
    """Базовая схема для работы с книгами."""

    title: Annotated[str, MinLen(3), MaxLen(100)] = Field(
        ...,
        title="Название книги",
        description="Название книги, длиной от 3 до 100 символов.",
        json_schema_extra={"example": "Война и Мир"},
    )
    description: Optional[Annotated[str, MaxLen(1000)]] = Field(
        None,
        title="Описание книги",
        description="Описание книги, длиной до 1000 символов.",
        json_schema_extra={"example": "Роман, описывающий..."},
    )
    publication_date: date = Field(
        ...,
        title="Дата публикации",
        description="Дата публикации книги.",
        json_schema_extra={"example": "1869-01-01"},
    )
    genre: Annotated[str, MinLen(3), MaxLen(50)] = Field(
        ...,
        title="Жанр",
        description="Жанр книги, длиной от 3 до 50 символов.",
        json_schema_extra={"example": "Роман"},
    )
    available_copies: int = Field(
        ...,
        ge=0,
        title="Доступные экземпляры",
        description="Количество доступных экземпляров книги (>= 0).",
        json_schema_extra={"example": 5},
    )


class BookCreate(BookBase):
    """Схема для создания книги."""

    author_ids: List[int] = Field(
        ...,
        title="Идентификаторы авторов",
        description="Список ID авторов книги.",
        json_schema_extra={"example": [1, 2, 3]},
    )


class BookResponse(BookBase):
    """Схема для ответа с данными книги."""

    id: int = Field(
        ...,
        title="ID книги",
        description="Уникальный идентификатор книги.",
        json_schema_extra={"example": 1},
    )
    authors: List[str] = Field(
        ...,
        title="Авторы книги",
        description="Список имен авторов книги.",
        json_schema_extra={"example": ["Лев Толстой", "Фёдор Достоевский"]},
    )

    model_config = ConfigDict(from_attributes=True)

    @field_validator("authors", mode="before")
    def convert_authors(cls, value):  # noqa
        """Конвертирует объекты авторов в их имена."""

        return [author.name for author in value]
