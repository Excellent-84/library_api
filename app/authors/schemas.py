"""
Pydantic-схемы для работы с авторами:

- Валидация данных авторов (создание, обновление).
- Формирование ответа API с информацией об авторах.
"""

from datetime import date
from typing import Annotated, Optional

from annotated_types import MaxLen, MinLen
from pydantic import BaseModel, ConfigDict, Field


class AuthorBase(BaseModel):
    """Базовая схема автора."""

    name: Annotated[str, MinLen(3), MaxLen(50)] = Field(
        ...,
        title="Имя автора",
        description="Имя автора должно содержать от 3 до 50 символов.",
        json_schema_extra={"example": "Лев Толстой"},
    )
    birth_date: date = Field(
        ...,
        title="Дата рождения",
        description="Дата рождения автора в формате ГГГГ-ММ-ДД.",
        json_schema_extra={"example": "1828-09-09"},
    )
    biography: Optional[Annotated[str, MaxLen(1000)]] = Field(
        None,
        title="Биография",
        description="Краткая биография автора (до 1000 символов).",
        json_schema_extra={"example": "Автор произведения 'Войнв и Мир'."},
    )


class AuthorCreate(AuthorBase):
    """Схема для создания нового автора."""

    pass


class AuthorUpdate(BaseModel):
    """Схема для обновления данных автора."""

    name: Optional[Annotated[str, MinLen(3), MaxLen(50)]] = Field(
        None,
        title="Новое имя автора",
        description="Имя автора должно содержать от 3 до 50 символов.",
        json_schema_extra={"example": "Фёдор Достоевский"},
    )
    birth_date: Optional[date] = Field(
        None,
        title="Новая дата рождения",
        description="Дата рождения автора в формате ГГГГ-ММ-ДД.",
        json_schema_extra={"example": "1821-11-11"},
    )
    biography: Optional[Annotated[str, MaxLen(1000)]] = Field(
        None,
        title="Новая биография",
        description="Краткая биография автора (до 1000 символов).",
        json_schema_extra={
            "example": "Автор произведения 'Преступление и наказание'."
        },
    )


class AuthorRead(AuthorBase):
    """Схема для ответа с данными автора."""

    id: int = Field(
        ...,
        title="ID автора",
        description="Уникальный идентификатор автора.",
        json_schema_extra={"example": 1},
    )

    model_config = ConfigDict(from_attributes=True)
