from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_async_session
from .exceptions import LoginException, UserExistsException
from .schemas import Token, UserCreate, UserResponse
from .security import create_access_token
from .services import authenticate_user, create_user, get_current_user

users_router = APIRouter(prefix="/users", tags=["Users"])


@users_router.post("/register", response_model=UserResponse, status_code=201)
async def register(
    user: UserCreate, db: AsyncSession = Depends(get_async_session)
):
    existing_user = await authenticate_user(db, user.username, user.password)

    if existing_user:
        raise UserExistsException

    return await create_user(db, user.username, user.email, user.password)


@users_router.post("/login", response_model=Token)
async def login(
    username: str, password: str, db: AsyncSession = Depends(get_async_session)
):
    user = await authenticate_user(db, username, password)

    if not user:
        raise LoginException

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token}


@users_router.get("/me")
async def user_profile(current_user: UserResponse = Depends(get_current_user)):
    return current_user
