from datetime import datetime, timedelta

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..books import Book
from ..users import BaseModel, User


class Rebook(BaseModel):
    """Модель выдачи книг."""

    __tablename__ = "rebooks"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        doc="ID пользователя, которому выдана книга",
    )
    book_id: Mapped[int] = mapped_column(
        ForeignKey("books.id"),
        nullable=False,
        doc="ID книги, которая была выдана",
    )
    borrowed_at: Mapped[datetime] = mapped_column(
        default=func.now(),
        server_default=func.now(),
        nullable=False,
        doc="Дата и время выдачи книги",
    )
    due_date: Mapped[datetime] = mapped_column(
        default=func.now() + timedelta(days=14),
        nullable=False,
        doc="Срок возврата книги (по умолчанию 14 дней)",
    )
    returned_at: Mapped[datetime] = mapped_column(
        nullable=True, doc="Дата и время возврата книги"
    )

    user = relationship(
        "User",
        back_populates="rebooks",
        doc="Связь с пользователем, которому выдана книга",
    )
    book = relationship(
        "Book",
        back_populates="rebooks",
        doc="Связь с книгой, которая была выдана",
    )


User.rebooks = relationship(
    "Rebook",
    back_populates="user",
    cascade="all, delete-orphan",
    doc="Список выдач, связанных с пользователем",
)
Book.rebooks = relationship(
    "Rebook",
    back_populates="book",
    cascade="all, delete-orphan",
    doc="Список выдач, связанных с книгой",
)
