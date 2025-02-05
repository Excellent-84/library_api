from datetime import date

from sqlalchemy import Column, Date, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..users import BaseModel

book_author = Table(
    "book_author",
    BaseModel.metadata,
    Column("book_id", ForeignKey("books.id"), primary_key=True),
    Column("author_id", ForeignKey("authors.id"), primary_key=True),
)


class Book(BaseModel):
    """Модель книги."""

    __tablename__ = "books"

    title: Mapped[str] = mapped_column(
        String(100), nullable=False, doc="Название книги"
    )
    description: Mapped[str] = mapped_column(
        Text, nullable=True, doc="Описание книги"
    )
    publication_date: Mapped[date] = mapped_column(
        Date, nullable=False, doc="Дата публикации книги"
    )
    genre: Mapped[str] = mapped_column(
        String(50), nullable=False, doc="Жанр книги"
    )
    available_copies: Mapped[int] = mapped_column(
        Integer,
        default=1,
        nullable=False,
        doc="Количество доступных экземпляров книги",
    )

    authors = relationship(
        "Author",
        secondary=book_author,
        back_populates="books",
        lazy="selectin",
        doc="Связь с авторами книги через промежуточную таблицу book_author",
    )
