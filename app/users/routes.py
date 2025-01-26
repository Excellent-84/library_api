from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..database import get_async_session
from .enums import UserRole
from .models import User
from .schemas import (
    LoginRequest,
    RoleUpdate,
    Token,
    UserCreate,
    UserResponse,
    UserUpdate,
)
from .services import (
    create_user,
    get_current_user,
    login_user,
    require_role,
    update_current_user,
    update_user_role,
)

users_router = APIRouter(prefix="/users", tags=["Users"])


@users_router.post("/register", response_model=UserResponse, status_code=201)
async def register(
    user: UserCreate, db: AsyncSession = Depends(get_async_session)
):
    return await create_user(user, db)


@users_router.post("/login", response_model=Token)
async def login(
    data: LoginRequest, db: AsyncSession = Depends(get_async_session)
):
    return await login_user(data, db)


@users_router.get("/", response_model=list[UserResponse])
async def list_users(
    db: AsyncSession = Depends(get_async_session),
    current_user=Depends(require_role(UserRole.ADMIN)),
):
    result = await db.execute(select(User))
    return result.scalars().all() or []


@users_router.get("/me", response_model=UserResponse)
async def get_me(current_user: UserResponse = Depends(get_current_user)):
    return current_user


@users_router.put("/me/update", response_model=UserResponse)
async def update_me(
    user_update: UserUpdate,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    return await update_current_user(user_update, db, current_user)


@users_router.put("/{user_id}/role", response_model=dict)
async def update_role(
    user_id: int,
    role_update: RoleUpdate,
    db: AsyncSession = Depends(get_async_session),
    current_user=Depends(require_role(UserRole.ADMIN)),
):
    return await update_user_role(user_id, role_update, db)
