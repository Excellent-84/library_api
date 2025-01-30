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
    __tablename__ = "books"

    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    publication_date: Mapped[date] = mapped_column(Date, nullable=False)
    genre: Mapped[str] = mapped_column(String(50), nullable=False)
    available_copies: Mapped[int] = mapped_column(
        Integer, default=1, nullable=False
    )

    authors = relationship(
        "Author",
        secondary=book_author,
        back_populates="books",
        lazy="selectin",
    )
