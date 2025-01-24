from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..authors import Author
from .exceptions import BookNotFoundException
from .models import Book
from .schemas import BookCreate


async def create_book(book_data: BookCreate, db: AsyncSession) -> Book:
    authors = await db.execute(
        select(Author).filter(Author.id.in_(book_data.author_ids))
    )
    authors = authors.scalars().all()

    if len(authors) != len(book_data.author_ids):
        raise BookNotFoundException

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
    book = await db.scalar(select(Book).filter(Book.id == book_id))
    if not book:
        raise BookNotFoundException
    return book


async def update_book(
    book_id: int, book_data: BookCreate, db: AsyncSession
) -> Book:
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
    book = await get_book_by_id(book_id, db)
    await db.delete(book)
    await db.commit()
