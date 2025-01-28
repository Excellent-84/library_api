from fastapi import HTTPException
from sqlalchemy import asc, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..books import Book
from .models import Rebook


async def borrow_book(db: AsyncSession, user_id: int, book_id: int) -> Rebook:
    book = await db.scalar(select(Book).filter(Book.id == book_id))

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    if book.available_copies < 1:
        raise HTTPException(status_code=400, detail="No copies available")

    user_rebooks_count = await db.scalar(
        select(func.count(Rebook.id)).filter(
            Rebook.user_id == user_id, Rebook.returned_at.is_(None)
        )
    )
    if user_rebooks_count >= 5:
        raise HTTPException(
            status_code=400, detail="User has reached the borrowing limit"
        )

    rebook = Rebook(user_id=user_id, book_id=book_id)
    book.available_copies -= 1

    db.add(rebook)
    db.add(book)
    await db.commit()
    await db.refresh(rebook)
    return rebook


async def return_book(db: AsyncSession, user_id: int, book_id: int) -> Rebook:
    rebook = await db.scalar(
        select(Rebook).filter(
            Rebook.user_id == user_id,
            Rebook.book_id == book_id,
            Rebook.returned_at.is_(None),
        )
    )

    if not rebook:
        raise HTTPException(status_code=404, detail="Rebook record not found")

    rebook.returned_at = func.now()
    book = await db.scalar(select(Book).filter(Book.id == book_id))
    book.available_copies += 1

    db.add(rebook)
    db.add(book)
    await db.commit()
    await db.refresh(rebook)
    return rebook


async def get_all_rebooks(db: AsyncSession) -> list[Rebook]:
    result = await db.execute(select(Rebook).order_by(asc(Rebook.id)))
    return result.scalars().all()
