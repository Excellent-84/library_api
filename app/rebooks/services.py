"""
Вспомогательные функции для работы с выданными книгами пользователям:

- Выдача и возврат книг.
- Получение информации о выданных книгах.
"""

from sqlalchemy import asc, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..books import get_book_by_id
from .exceptions import (
    AvailableException,
    LimitException,
    RebookNotFoundException,
)
from .models import Rebook


async def borrow_book(db: AsyncSession, user_id: int, book_id: int) -> Rebook:
    """
    Выдача книги пользователю.
    Возвращает информацию о выданной книге.
    Выбрасывает исключение, если книга недоступна или
    если пользователь превысил лимит на выдачу.
    """

    book = await get_book_by_id(book_id, db)

    if book.available_copies < 1:
        raise AvailableException()

    user_rebooks_count = await db.scalar(
        select(func.count(Rebook.id)).filter(
            Rebook.user_id == user_id, Rebook.returned_at.is_(None)
        )
    )

    if user_rebooks_count >= 5:
        raise LimitException()

    rebook = Rebook(user_id=user_id, book_id=book_id)
    book.available_copies -= 1

    db.add(rebook)
    db.add(book)
    await db.commit()
    await db.refresh(rebook)
    return rebook


async def get_rebook_by_id(rebook_id: int, db: AsyncSession) -> Rebook:
    """
    Получение информации о выданной книге по ID.
    Возвращает информацию о выдаче книги.
    Выбрасывает исключение, если выдача книги не найдена.
    """

    rebook = await db.scalar(select(Rebook).filter(Rebook.id == rebook_id))

    if not rebook:
        raise RebookNotFoundException()

    return rebook


async def return_book(db: AsyncSession, user_id: int, book_id: int) -> Rebook:
    """
    Возврат книги пользователем.
    Обновляет статус выдачи и увеличивает количество доступных копий книги.
    Возвращает информацию о выданной книге.
    Выбрасывает исключение, если книга не была выдана пользователю.
    """
    rebook = await db.scalar(
        select(Rebook).filter(
            Rebook.user_id == user_id,
            Rebook.book_id == book_id,
            Rebook.returned_at.is_(None),
        )
    )

    if not rebook:
        raise RebookNotFoundException()

    if rebook.returned_at is not None:
        raise RebookNotFoundException()

    rebook.returned_at = func.now()
    book = await get_book_by_id(book_id, db)
    book.available_copies += 1

    db.add(rebook)
    db.add(book)
    await db.commit()
    await db.refresh(rebook)
    return rebook


async def get_all_rebooks(
    db: AsyncSession,
    limit: int = 10,
    offset: int = 0,
    user_id: int | None = None,
) -> list[Rebook]:
    """
    Получение списка всех выданных книг с возможностью фильтрации и пагинации.
    Возвращает список выданных книг.
    """
    query = select(Rebook).order_by(asc(Rebook.id))
    if user_id:
        query = query.filter(Rebook.user_id == user_id)

    query = query.limit(limit).offset(offset)
    result = await db.execute(query)
    return result.scalars().all()
