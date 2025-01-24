from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..database import get_async_session
from ..users import UserRole, require_role
from .models import Author
from .schemas import AuthorCreate, AuthorRead, AuthorUpdate
from .services import author_create, get_author_by_id
from .utils import update_instance

authors_router = APIRouter(prefix="/authors", tags=["Authors"])


@authors_router.post("/", response_model=AuthorRead, status_code=201)
async def create_author(
    author: AuthorCreate,
    db: AsyncSession = Depends(get_async_session),
    current_user=Depends(require_role(UserRole.ADMIN)),
):
    return await author_create(author, db)


@authors_router.get("/", response_model=list[AuthorRead])
async def get_authors(
    db: AsyncSession = Depends(get_async_session),
):
    result = await db.execute(select(Author))
    return result.scalars().all()


@authors_router.get("/{author_id}", response_model=AuthorRead)
async def get_author(
    author_id: int, db: AsyncSession = Depends(get_async_session)
):
    return await get_author_by_id(author_id, db)


@authors_router.put("/{author_id}", response_model=AuthorRead)
async def update_author(
    author_id: int,
    author_update: AuthorUpdate,
    db: AsyncSession = Depends(get_async_session),
    current_user=Depends(require_role(UserRole.ADMIN)),
):
    author = await get_author_by_id(author_id, db)
    update_instance(author, author_update.model_dump(exclude_unset=True))

    db.add(author)
    await db.commit()
    await db.refresh(author)
    return author


@authors_router.delete("/{author_id}", status_code=204)
async def delete_author(
    author_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user=Depends(require_role(UserRole.ADMIN)),
):
    author = await get_author_by_id(author_id, db)
    await db.delete(author)
    await db.commit()
