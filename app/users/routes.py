from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..database import get_async_session
from .enums import UserRole
from .exceptions import (
    LoginException,
    UserExistsException,
    UserNotFoundException,
)
from .models import User
from .schemas import LoginRequest, RoleUpdate, Token, UserCreate, UserResponse
from .security import create_access_token
from .services import (
    authenticate_user,
    create_user,
    get_current_user,
    require_role,
)

users_router = APIRouter(prefix="/users", tags=["Users"])


@users_router.post("/register", response_model=UserResponse, status_code=201)
async def register(
    user: UserCreate, db: AsyncSession = Depends(get_async_session)
):
    if await db.scalar(select(User).filter(User.username == user.username)):
        raise UserExistsException

    return await create_user(db, user.username, user.email, user.password)


@users_router.post("/login", response_model=Token)
async def login(
    data: LoginRequest, db: AsyncSession = Depends(get_async_session)
):
    user = await authenticate_user(db, data.username, data.password)

    if not user:
        raise LoginException

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@users_router.get("/me", response_model=UserResponse)
async def get_me(current_user: UserResponse = Depends(get_current_user)):
    return current_user


@users_router.put("/me/update", response_model=UserResponse)
async def update_me(
    user_update: UserCreate,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    current_user.username = user_update.username
    current_user.email = user_update.email
    db.add(current_user)
    await db.commit()
    await db.refresh(current_user)
    return current_user


@users_router.get("/", response_model=list[UserResponse])
async def list_users(
    db: AsyncSession = Depends(get_async_session),
    current_user=Depends(require_role(UserRole.ADMIN)),
):
    result = await db.execute(select(User))
    return result.scalars().all() or []


@users_router.put("/{user_id}/role", response_model=dict)
async def update_role(
    user_id: int,
    role_update: RoleUpdate,
    db: AsyncSession = Depends(get_async_session),
    current_user=Depends(require_role(UserRole.ADMIN)),
):
    user = await db.scalar(select(User).filter(User.id == user_id))

    if not user:
        raise UserNotFoundException

    user.role = role_update.new_role
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return {"message": f"Role updated to {role_update.new_role}"}
