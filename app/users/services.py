"""
Вспомогательные функции для работы с пользователями:

- Регистрация пользователей.
- Аутентификация пользователей.
- Управление ролями пользователей.
- Получение данных о пользователях.
"""

from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy import asc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from ..database import get_async_session, settings
from .enums import UserRole
from .exceptions import (
    CredentialsException,
    LoginException,
    PermissionException,
    UserExistsException,
    UserNotFoundException,
)
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
from .security import create_access_token, get_password_hash, verify_password

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/users/login",
    description="JWT токен передаётся в формате: `Bearer <token>`",
)


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    """
    Получение пользователя по email. Возвращает пользователя, иначе None.
    """

    query = select(User).filter(User.email == email)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def create_user(user: UserCreate, db: AsyncSession) -> UserResponse:
    """
    Создание нового пользователя.
    Первому зарегистрированному пользователю присваивается роль "admin",
    всем последующим - "reader".
    Возвращает ответ с информацией о созданном пользователе.
    Выбрасывает исключение, если пользователь с таким email уже существует.
    """

    if await get_user_by_email(db, user.email):
        raise UserExistsException()

    hashed_password = get_password_hash(user.password)
    role = (
        UserRole.ADMIN.value
        if not (await db.scalar(select(User.id).limit(1)))
        else UserRole.READER.value
    )

    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        role=role,
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def authenticate_user(
    db: AsyncSession, email: str, password: str
) -> User | None:
    """
    Проверяет, существует ли пользователь с таким email и паролем.
    Возвращает пользователя, если аутентификация прошла успешно, иначе None.
    """

    user = await get_user_by_email(db, email)

    if user and verify_password(password, user.hashed_password):
        return user

    return None


async def login_user(data: LoginRequest, db: AsyncSession) -> Token:
    """
    Аутентификация пользователя и создание токен доступа.
    Возвращает токен доступа для пользователя.
    Выбрасывает исключение, если аутентификация не удалась.
    """

    user = await authenticate_user(db, data.email, data.password)

    if not user:
        raise LoginException()

    access_token = create_access_token(data={"sub": user.email})
    return Token(access_token=access_token)


async def get_user_by_id(user_id: int, db: AsyncSession) -> UserRebookResponse:
    """
    Получение пользователя по ID.
    Возвращает информация о пользователе и выданных ему книгах.
    Выбрасывает исключение, если пользователь не найден.
    """

    query = (
        select(User)
        .options(joinedload(User.rebooks))
        .filter(User.id == user_id)
    )
    result = await db.execute(query)
    user = result.unique().scalar_one_or_none()

    if not user:
        raise UserNotFoundException()

    user_response = UserRebookResponse.model_validate(user)
    user_response.set_rebooks(user.rebooks)
    return user_response


async def get_all_users(db: AsyncSession) -> list[UserResponse]:
    """
    Получение списка всех пользователей.
    Возвращает список пользователей.
    """

    result = await db.execute(select(User).order_by(asc(User.id)))
    return result.scalars().all()


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: AsyncSession = Depends(get_async_session),
) -> User:
    """
    Получает текущего аутентифицированного пользователя по токену.
    Возвращает аутентифицированного пользователя.
    Выбрасывает исключение, если токен недействителен или пользователь
    не найден.
    """

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get("sub")

        if not email:
            raise CredentialsException()

    except JWTError:
        raise CredentialsException()

    user = await get_user_by_email(db, email)

    if not user:
        raise UserNotFoundException()

    return user


async def update_current_user(
    user_update: UserUpdate, db: AsyncSession, current_user: User
) -> UserResponse:
    """
    Обновляет данные текущего пользователя.
    Возвращает обновленную информация о пользователе.
    """

    if user_update.username:
        current_user.username = user_update.username

    if user_update.password:
        current_user.hashed_password = get_password_hash(user_update.password)

    db.add(current_user)
    await db.commit()
    await db.refresh(current_user)
    return current_user


async def update_user_role(
    user_id: int, role_update: RoleUpdate, db: AsyncSession
) -> dict:
    """
    Обновляет роль пользователя.
    Возвращает сообщение об успешном обновлении роли.
    Выбрасывает исключение, если пользователь не найден.
    """

    user = await db.scalar(select(User).filter(User.id == user_id))

    if not user:
        raise UserNotFoundException()

    user.role = role_update.new_role
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return {"message": f"Role updated to {role_update.new_role}"}


def require_role(role: str):
    """
    Декоратор для проверки роли пользователя.
    Возвращает текущего пользователя, если роль совпадает.
    Выбрасывает исключение, если роль пользователя не совпадает с требуемой.
    """

    def check_role(current_user=Depends(get_current_user)):
        if current_user.role != role:
            raise PermissionException()
        return current_user

    return check_role
