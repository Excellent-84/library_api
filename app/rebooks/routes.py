from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_async_session
from ..users import UserRole, get_current_user, require_role
from .schemas import RebookBase, RebookResponse
from .services import (
    borrow_book,
    get_all_rebooks,
    get_rebook_by_id,
    return_book,
)

rebooks_router = APIRouter(prefix="/rebooks", tags=["Rebooks"])


@rebooks_router.post(
    "/",
    response_model=RebookResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Выдача книги",
    description="Пользователь может забронировать книгу.",
    responses={
        201: {"description": "Книга успешно выдана."},
        400: {"description": "Некорректные данные для выдачи."},
        404: {"description": "Книга не найдена или недоступна."},
        403: {"description": "Превышен лимит выдачи книг."},
    },
)
async def borrow(
    rebook_data: RebookBase,
    db: AsyncSession = Depends(get_async_session),
    current_user=Depends(get_current_user),
):
    return await borrow_book(db, current_user.id, rebook_data.book_id)


@rebooks_router.post(
    "/return",
    response_model=RebookResponse,
    summary="Возврат книги",
    description="Пользователь может вернуть книгу.",
    responses={
        200: {"description": "Книга успешно возвращена."},
        404: {"description": "Выдача книги не найдена."},
    },
)
async def return_rebook(
    rebook_data: RebookBase,
    db: AsyncSession = Depends(get_async_session),
    current_user=Depends(get_current_user),
):
    return await return_book(db, current_user.id, rebook_data.book_id)


@rebooks_router.get(
    "/",
    response_model=list[RebookResponse],
    summary="Список выданных книг",
    description="""
    Получение списка всех выданных книг (только для администратора).
    - Можно задать `limit` (количество выданных книг) и `offset`
    (начало выборки).
    - Можно фильтровать по `user_id`.
    """,
    responses={
        200: {"description": "Список выданных книг успешно получен."},
        403: {"description": "Недостаточно прав для выполнения операции."},
    },
)
async def get_rebooks(
    limit: int = Query(10, ge=1, le=100, description="Количество записей."),
    offset: int = Query(0, ge=0, description="Смещение от начала выборки."),
    user_id: int | None = Query(None, description="Фильтр по пользователю."),
    db: AsyncSession = Depends(get_async_session),
    current_user=Depends(require_role(UserRole.ADMIN)),
):
    return await get_all_rebooks(
        db=db, limit=limit, offset=offset, user_id=user_id
    )


@rebooks_router.get(
    "/{rebook_id}",
    response_model=RebookResponse,
    summary="Получение выдачи книги по ID",
    description="""
    Получение данных о выдаче книги по ID (только для администратора).
    """,
    responses={
        200: {"description": "Данные о выдаче успешно получены."},
        404: {"description": "Выдача книг с указанным ID не найдено."},
        403: {"description": "Недостаточно прав для выполнения операции."},
    },
)
async def get_rebook(
    rebook_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user=Depends(require_role(UserRole.ADMIN)),
):
    return await get_rebook_by_id(rebook_id, db)
