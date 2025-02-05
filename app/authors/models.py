from datetime import date

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Date, Text

from ..users import BaseModel


class Author(BaseModel):
    """Модель автора."""

    __tablename__ = "authors"

    name: Mapped[str] = mapped_column(
        String(60), unique=True, nullable=False, doc="Имя автора"
    )
    biography: Mapped[str] = mapped_column(
        Text, nullable=True, doc="Биография автора"
    )
    birth_date: Mapped[date] = mapped_column(
        Date, nullable=False, doc="Дата рождения автора"
    )

    books = relationship(
        "Book",
        secondary="book_author",
        back_populates="authors",
        doc="Список книг, написанных автором (отношение 'многие ко многим')",
    )
