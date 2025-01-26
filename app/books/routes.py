from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_async_session
from ..users import UserRole, require_role
from .schemas import BookCreate, BookResponse
from .services import create_book, delete_book, get_book_by_id, update_book

books_router = APIRouter(prefix="/books", tags=["Books"])


@books_router.post("/", response_model=BookResponse, status_code=201)
async def add_book(
    book: BookCreate,
    db: AsyncSession = Depends(get_async_session),
    current_user=Depends(require_role(UserRole.ADMIN)),
):
    return await create_book(book, db)


@books_router.get("/{book_id}", response_model=BookResponse)
async def get_book(
    book_id: int, db: AsyncSession = Depends(get_async_session)
):
    return await get_book_by_id(book_id, db)


@books_router.put("/{book_id}", response_model=BookResponse)
async def update(
    book_id: int,
    book: BookCreate,
    db: AsyncSession = Depends(get_async_session),
    current_user=Depends(require_role(UserRole.ADMIN)),
):
    return await update_book(book_id, book, db)


@books_router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    book_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user=Depends(require_role(UserRole.ADMIN)),
):
    await delete_book(book_id, db)
