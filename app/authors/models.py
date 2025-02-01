from datetime import date

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Date, Text

from ..users import BaseModel


class Author(BaseModel):
    __tablename__ = "authors"

    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    biography: Mapped[str] = mapped_column(Text, nullable=True)
    birth_date: Mapped[date] = mapped_column(Date, nullable=False)

    books = relationship(
        "Book", secondary="book_author", back_populates="authors"
    )
