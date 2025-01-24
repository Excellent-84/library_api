from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from .exceptions import AuthorExistsException, AuthorNotFoundException
from .models import Author
from .schemas import AuthorCreate


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
