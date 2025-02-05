from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_async_session
from ..users import UserRole, require_role
from .schemas import BookCreate, BookResponse
from .services import (
    create_book,
    delete_book,
    get_all_books,
    get_book_by_id,
    update_book,
)

books_router = APIRouter(prefix="/books", tags=["Books"])


@books_router.post(
    "/",
    response_model=BookResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Добавление новой книги",
    description="Добавляет новую книгу (только для администратора).",
    responses={
        201: {"description": "Книга успешно добавлена."},
        400: {"description": "Некорректные данные для добавления книги."},
        403: {"description": "Недостаточно прав для выполнения операции."},
    },
)
async def add_book(
    book: BookCreate,
    db: AsyncSession = Depends(get_async_session),
    current_user=Depends(require_role(UserRole.ADMIN)),
):
    return await create_book(book, db)


@books_router.get(
    "/",
    response_model=list[BookResponse],
    summary="Получение списка книг",
    description="""
    Получение списка всех книг.
    - Можно задать `limit` (количество книг) и `offset` (начало выборки).
    - Можно фильтровать книги по жанру.
    """,
    responses={
        200: {"description": "Список книг успешно получен."},
        400: {"description": "Некорректные параметры запроса."},
    },
)
async def get_books(
    limit: int = Query(10, ge=1, le=100, description="Количество записей."),
    offset: int = Query(0, ge=0, description="Смещение от начала выборки."),
    genre: str | None = Query(
        None, max_length=50, description="Фильтр по жанру."
    ),
    db: AsyncSession = Depends(get_async_session),
):
    return await get_all_books(db=db, limit=limit, offset=offset, genre=genre)


@books_router.get(
    "/{book_id}",
    response_model=BookResponse,
    summary="Получение книги по ID",
    description="Получение данных о книге по ее ID",
    responses={
        200: {"description": "Информация о книге успешно получена."},
        404: {"description": "Книга с указанным ID не найдена."},
    },
)
async def get_book(
    book_id: int, db: AsyncSession = Depends(get_async_session)
):
    return await get_book_by_id(book_id, db)


@books_router.put(
    "/{book_id}",
    response_model=BookResponse,
    summary="Обновление данных о книге",
    description="Обновление информации о книге (только для администратора).",
    responses={
        200: {"description": "Данные книги успешно обновлены."},
        400: {"description": "Некорректные данные для обновления."},
        404: {"description": "Книга с указанным ID не найдена."},
        403: {"description": "Недостаточно прав для выполнения операции."},
    },
)
async def update(
    book_id: int,
    book: BookCreate,
    db: AsyncSession = Depends(get_async_session),
    current_user=Depends(require_role(UserRole.ADMIN)),
):
    return await update_book(book_id, book, db)


@books_router.delete(
    "/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удаление книги",
    description="Удаляет книгу по ID (только для администратора)",
    responses={
        204: {"description": "Книга успешно удалена."},
        404: {"description": "Книга с указанным ID не найдена."},
        403: {"description": "Недостаточно прав для выполнения операции."},
    },
)
async def delete(
    book_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user=Depends(require_role(UserRole.ADMIN)),
):
    await delete_book(book_id, db)
