from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_async_session
from .enums import UserRole
from .models import User
from .schemas import (
    LoginRequest,
    RoleUpdate,
    Token,
    UserCreate,
    UserRebookResponse,
    UserResponse,
    UserUpdate,
)
from .services import (
    create_user,
    get_all_users,
    get_current_user,
    get_user_by_id,
    login_user,
    require_role,
    update_current_user,
    update_user_role,
)

users_router = APIRouter(prefix="/users", tags=["Users"])


@users_router.post(
    "/register",
    response_model=UserResponse,
    status_code=201,
    summary="Регистрация пользователя",
    description="""
    Регистрирует нового пользователя.

    - Поля `username`, `email`, `password` и `role` обязательны.
    - По умолчанию роль пользователя — `reader`.
    - Только администратор может изменить роль пользователя.
    """,
    responses={
        201: {"description": "Пользователь успешно зарегистрирован."},
        400: {"description": "Некорректные данные для регистрации."},
    },
)
async def register(
    user: UserCreate, db: AsyncSession = Depends(get_async_session)
):
    return await create_user(user, db)


@users_router.post(
    "/login",
    response_model=Token,
    summary="Вход в систему",
    description="""
    Аутентификация пользователя с использованием email и пароля.
    Возвращает JWT токен для последующей авторизации.
    """,
    responses={
        200: {"description": "Успешная аутентификация."},
        401: {"description": "Неверные учетные данные."},
    },
)
async def login(
    data: LoginRequest, db: AsyncSession = Depends(get_async_session)
):
    return await login_user(data, db)


@users_router.get(
    "/",
    response_model=list[UserResponse],
    summary="Список пользователей",
    description="""
    Получение списка всех пользователей (только для администратора).
    """,
    responses={
        200: {"description": "Список пользователей успешно получен."},
        403: {"description": "Недостаточно прав для выполнения операции."},
    },
)
async def list_users(
    db: AsyncSession = Depends(get_async_session),
    current_user=Depends(require_role(UserRole.ADMIN)),
):
    return await get_all_users(db)


@users_router.get(
    "/me",
    response_model=UserRebookResponse,
    summary="Информация о текущем пользователе",
    description="""
    Получение информации о текущем пользователе.
    Возвращает данные о текущем пользователе и выданных ему книгах.
    """,
    responses={
        200: {"description": "Данные текущего пользователя успешно получены."},
        401: {"description": "Необходима авторизация."},
    },
)
async def get_me(
    db: AsyncSession = Depends(get_async_session),
    current_user: UserRebookResponse = Depends(get_current_user),
):
    return await get_user_by_id(current_user.id, db)


@users_router.put(
    "/me",
    response_model=UserResponse,
    summary="Обновление данных текущего пользователя",
    description="""
    Позволяет текущему пользователю обновить свои данные,
    такие как `username` и `password`.
    """,
    responses={
        200: {"description": "Данные пользователя успешно обновлены."},
        400: {"description": "Некорректные данные для обновления."},
        401: {"description": "Необходима авторизация."},
    },
)
async def update_me(
    user_update: UserUpdate,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    return await update_current_user(user_update, db, current_user)


@users_router.get(
    "/{user_id}",
    response_model=UserRebookResponse,
    summary="Получение данных пользователя по ID",
    description="""
    Получение информации о пользователе по ID (только для администратора).
    Возвращает данные о пользователе  и выданных ему книгах.
    """,
    responses={
        200: {"description": "Данные пользователя успешно получены."},
        404: {"description": "Пользователь с указанным ID не найден."},
        403: {"description": "Недостаточно прав для выполнения операции."},
    },
)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user=Depends(require_role(UserRole.ADMIN)),
):
    return await get_user_by_id(user_id, db)


@users_router.put(
    "/{user_id}/role",
    response_model=dict,
    summary="Обновление роли пользователя",
    description="""
    Обновление роли пользователя (только для администратора).
    Возвращает сообщение об успешном обновлении роли пользователя.
    """,
    responses={
        200: {"description": "Роль пользователя успешно обновлена."},
        404: {"description": "Пользователь с указанным ID не найден."},
        403: {"description": "Недостаточно прав для выполнения операции."},
    },
)
async def update_role(
    user_id: int,
    role_update: RoleUpdate,
    db: AsyncSession = Depends(get_async_session),
    current_user=Depends(require_role(UserRole.ADMIN)),
):
    return await update_user_role(user_id, role_update, db)
