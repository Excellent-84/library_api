from datetime import datetime, timedelta

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..books import Book
from ..users import BaseModel, User


class Rebook(BaseModel):
    __tablename__ = "rebooks"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False
    )
    book_id: Mapped[int] = mapped_column(
        ForeignKey("books.id"), nullable=False
    )
    borrowed_at: Mapped[datetime] = mapped_column(
        default=func.now(), server_default=func.now(), nullable=False
    )
    due_date: Mapped[datetime] = mapped_column(
        default=func.now() + timedelta(days=14), nullable=False
    )
    returned_at: Mapped[datetime] = mapped_column(nullable=True)

    user = relationship("User", back_populates="rebooks")
    book = relationship("Book", back_populates="rebooks")


User.rebooks = relationship(
    "Rebook", back_populates="user", cascade="all, delete-orphan"
)
Book.rebooks = relationship(
    "Rebook", back_populates="book", cascade="all, delete-orphan"
)
