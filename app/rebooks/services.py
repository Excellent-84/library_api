from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..books import Book
from .models import Rebook


async def borrow_book(db: AsyncSession, user_id: int, book_id: int) -> Rebook:
    # Проверяем, существует ли книга
    book = await db.scalar(select(Book).filter(Book.id == book_id))
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    # Проверяем, доступна ли книга
    if book.available_copies < 1:
        raise HTTPException(status_code=400, detail="No copies available")

    # Проверяем, сколько книг у пользователя уже взято
    user_rebooks_count = await db.scalar(
        select(Rebook)
        .filter(Rebook.user_id == user_id, Rebook.returned_at is None)
        .count()
    )
    if user_rebooks_count >= 5:
        raise HTTPException(
            status_code=400, detail="User has reached the borrowing limit"
        )

    # Создаем запись о выдаче книги
    rebook = Rebook(user_id=user_id, book_id=book_id)
    book.available_copies -= 1

    db.add(rebook)
    db.add(book)
    await db.commit()
    await db.refresh(rebook)
    return rebook


async def return_book(db: AsyncSession, user_id: int, book_id: int) -> Rebook:
    # Проверяем, есть ли выдача
    rebook = await db.scalar(
        select(Rebook).filter(
            Rebook.user_id == user_id,
            Rebook.book_id == book_id,
            Rebook.returned_at is None,
        )
    )
    if not rebook:
        raise HTTPException(status_code=404, detail="Rebook record not found")

    # Обновляем статус книги и запись о возврате
    rebook.returned_at = datetime.now(timezone.utc)
    book = await db.scalar(select(Book).filter(Book.id == book_id))
    book.available_copies += 1

    db.add(rebook)
    db.add(book)
    await db.commit()
    await db.refresh(rebook)
    return rebook
