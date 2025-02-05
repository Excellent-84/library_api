"""
Вспомогательные функции для работы с книгами:

- Создание, обновление и удаление книг.
- Получение списка книг или данных о конкретной книге.
"""

from sqlalchemy import asc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..authors import Author
from .exceptions import BookNotFoundException
from .models import Book
from .schemas import BookCreate


async def create_book(book_data: BookCreate, db: AsyncSession) -> Book:
    """
    Создание новой книги.
    Возвращает ответ с информацией о созданной книге.
    Выбрасывает исключение, если авторы с указанными ID не найдены.
    """
    authors = await db.execute(
        select(Author).filter(Author.id.in_(book_data.author_ids))
    )
    authors = authors.scalars().all()

    if len(authors) != len(book_data.author_ids):
        raise BookNotFoundException()

    new_book = Book(
        title=book_data.title,
        description=book_data.description,
        publication_date=book_data.publication_date,
        genre=book_data.genre,
        available_copies=book_data.available_copies,
        authors=authors,
    )

    db.add(new_book)
    await db.commit()
    await db.refresh(new_book)
    return new_book


async def get_book_by_id(book_id: int, db: AsyncSession) -> Book:
    """
    Получение книги по ID.
    Возвращает информацию о книге.
    Выбрасывает исключение, если книга не найдена.
    """

    book = await db.scalar(select(Book).filter(Book.id == book_id))

    if not book:
        raise BookNotFoundException()

    return book


async def get_all_books(
    db: AsyncSession,
    limit: int = 10,
    offset: int = 0,
    genre: str | None = None,
) -> list[Book]:
    """
    Получение списка всех книг с пагинацией и фильтрацией по жанру.
    Возвращает список книг.
    """

    query = select(Book).order_by(asc(Book.id))
    if genre:
        query = query.filter(Book.genre.ilike(f"%{genre}%"))

    query = query.limit(limit).offset(offset)
    result = await db.execute(query)
    return result.scalars().all()


async def update_book(
    book_id: int, book_data: BookCreate, db: AsyncSession
) -> Book:
    """
    Обновляет информацию о книге.
    Возвращает обновленную информацию книгу.
    Выбрасывает исключение, если книга с указанным ID не найдена.
    """

    book = await get_book_by_id(book_id, db)
    authors = await db.execute(
        select(Author).filter(Author.id.in_(book_data.author_ids))
    )
    authors = authors.scalars().all()

    book.title = book_data.title
    book.description = book_data.description
    book.publication_date = book_data.publication_date
    book.genre = book_data.genre
    book.available_copies = book_data.available_copies
    book.authors = authors

    db.add(book)
    await db.commit()
    await db.refresh(book)
    return book


async def delete_book(book_id: int, db: AsyncSession) -> None:
    """
    Удаление книги по ID.
    Выбрасывает исключение, если книга с указанным ID не найдена.
    """

    book = await get_book_by_id(book_id, db)
    await db.delete(book)
    await db.commit()
