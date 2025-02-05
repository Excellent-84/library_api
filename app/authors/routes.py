from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_async_session
from ..users import UserRole, get_current_user, require_role
from .schemas import AuthorCreate, AuthorRead, AuthorUpdate
from .services import (
    author_create,
    delete_author,
    get_all_authors,
    get_author_by_id,
    update_author,
)

authors_router = APIRouter(prefix="/authors", tags=["Authors"])


@authors_router.post(
    "/",
    response_model=AuthorRead,
    status_code=status.HTTP_201_CREATED,
    summary="Создание нового автора",
    description="Регистрирует нового автора (только для администратора).",
    responses={
        201: {"description": "Автор успешно создан."},
        400: {"description": "Некорректные данные для создания автора."},
        403: {"description": "Недостаточно прав для выполнения операции."},
    },
)
async def create_author(
    author: AuthorCreate,
    db: AsyncSession = Depends(get_async_session),
    current_user=Depends(require_role(UserRole.ADMIN)),
):
    return await author_create(author, db)


@authors_router.get(
    "/",
    response_model=list[AuthorRead],
    summary="Получение списка авторов",
    description="""
    Получение списка всех авторов.
    - Можно задать `limit` (количество авторов) и `offset` (начало выборки).
    - Можно фильтровать по имени автора.
    """,
    responses={
        200: {"description": "Список авторов успешно получен."},
        400: {"description": "Некорректные параметры запроса."},
    },
)
async def get_authors(
    db: AsyncSession = Depends(get_async_session),
    limit: int = Query(10, ge=1, le=100, description="Количество записей."),
    offset: int = Query(0, ge=0, description="Смещение от начала выборки."),
    name: str | None = Query(
        None, min_length=3, max_length=50, description="Фильтр по имени."
    ),
    current_user=Depends(get_current_user),
):
    return await get_all_authors(db, limit=limit, offset=offset, name=name)


@authors_router.get(
    "/{author_id}/",
    response_model=AuthorRead,
    summary="Получение данных автора по ID",
    description="Получение информации об авторе по ID.",
    responses={
        200: {"description": "Данные автора успешно получены."},
        404: {"description": "Автор с указанным ID не найден."},
    },
)
async def get_author(
    author_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user=Depends(get_current_user),
):
    return await get_author_by_id(author_id, db)


@authors_router.put(
    "/{author_id}/",
    response_model=AuthorRead,
    summary="Обновление данных автора",
    description="Обновление данных автора (только для администратора).",
    responses={
        200: {"description": "Данные автора успешно обновлены."},
        400: {"description": "Некорректные данные для обновления автора."},
        403: {"description": "Недостаточно прав для выполнения операции."},
        404: {"description": "Автор с указанным ID не найден."},
    },
)
async def update(
    author_id: int,
    author_update: AuthorUpdate,
    db: AsyncSession = Depends(get_async_session),
    current_user=Depends(require_role(UserRole.ADMIN)),
):
    return await update_author(author_id, author_update, db)


@authors_router.delete(
    "/{author_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удаление автора",
    description="Удаление автора по ID (только для администратора).",
    responses={
        204: {"description": "Автор успешно удалён."},
        403: {"description": "Недостаточно прав для выполнения операции."},
        404: {"description": "Автор с указанным ID не найден."},
    },
)
async def delete(
    author_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user=Depends(require_role(UserRole.ADMIN)),
):
    await delete_author(author_id, db)
