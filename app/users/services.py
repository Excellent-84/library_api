from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..database import get_async_session, settings
from .exceptions import CredentialsException
from .models import User
from .schemas import TokenData, UserResponse
from .security import get_password_hash, verify_password

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


async def create_user(
    db: AsyncSession,
    username: str,
    email: str,
    password: str,
    is_admin: bool = False
) -> User:

    hashed_password = get_password_hash(password)
    new_user = User(
        username=username,
        email=email,
        hashed_password=hashed_password,
        is_admin=is_admin
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def get_user_by_username(db: AsyncSession, username: str) -> User | None:
    query = select(User).filter(User.username == username)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def authenticate_user(
    db: AsyncSession, username: str, password: str
) -> User | None:
    user = await get_user_by_username(db, username)

    if user and verify_password(password, user.hashed_password):
        return user
    return None


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: AsyncSession = Depends(get_async_session),
) -> UserResponse:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str | None = payload.get("sub")
        if username is None:
            raise CredentialsException
        token_data = TokenData(username=username)
    except JWTError:
        raise CredentialsException
    user = await get_user_by_username(db=db, username=token_data.username)

    if user is None:
        raise CredentialsException

    return user
