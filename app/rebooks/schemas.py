"""
Pydantic-схемы для работы с выдачей и возвратом книг (Rebook):

- Валидация данных выдачи книг.
- Формирование ответов API с информацией о выдаче.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class RebookBase(BaseModel):
    """Базовая схема для работы с выдачей книг."""

    book_id: int = Field(
        ...,
        title="ID книги",
        description="Уникальный идентификатор книги, которая была выдана.",
        json_schema_extra={"example": 1},
    )


class RebookResponse(RebookBase):
    """Схема для ответа с информацией о выдаче книги."""

    id: int = Field(
        ...,
        title="ID выдачи",
        description="Уникальный идентификатор записи о выдаче книги.",
        json_schema_extra={"example": 101},
    )
    borrowed_at: datetime = Field(
        ...,
        title="Дата выдачи",
        description="Дата и время, когда книга была выдана.",
        json_schema_extra={"example": "2025-02-02T10:00:00"},
    )
    due_date: datetime = Field(
        ...,
        title="Срок возврата",
        description="Дата и время, до которых книга должна быть возвращена.",
        json_schema_extra={"example": "2025-02-16T10:00:00"},
    )
    returned_at: Optional[datetime] = Field(
        None,
        title="Дата возврата",
        description="Дата и время, когда книга была возвращена, иначе `null`.",
        json_schema_extra={"example": "2025-02-14T15:00:00"},
    )
    user_id: int = Field(
        ...,
        title="ID пользователя",
        description="Уникальный идентификатор пользователя, взявшего книгу.",
        json_schema_extra={"example": 42},
    )

    model_config = ConfigDict(from_attributes=True)
