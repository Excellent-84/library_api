from sqlalchemy import asc
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from .exceptions import AuthorExistsException, AuthorNotFoundException
from .models import Author
from .schemas import AuthorCreate, AuthorUpdate
from .utils import update_instance


async def author_create(author_data: AuthorCreate, db: AsyncSession) -> Author:
    new_author = Author(**author_data.model_dump())
    db.add(new_author)

    try:
        await db.commit()
    except IntegrityError:
        raise AuthorExistsException

    await db.refresh(new_author)
    return new_author


async def get_author_by_id(author_id: int, db: AsyncSession) -> Author:
    result = await db.execute(select(Author).filter(Author.id == author_id))
    author = result.scalar_one_or_none()

    if not author:
        raise AuthorNotFoundException

    return author


async def get_all_authors(db: AsyncSession) -> list[Author]:
    result = await db.execute(select(Author).order_by(asc(Author.id)))
    return result.scalars().all()


async def update_author(
    author_id: int, author_update: AuthorUpdate, db: AsyncSession
) -> Author:
    author = await get_author_by_id(author_id, db)
    update_instance(author, author_update.model_dump(exclude_unset=True))

    db.add(author)
    await db.commit()
    await db.refresh(author)
    return author


async def delete_author(author_id: int, db: AsyncSession) -> None:
    author = await get_author_by_id(author_id, db)
    await db.delete(author)
    await db.commit()
