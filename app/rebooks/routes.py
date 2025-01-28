from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_async_session
from ..users import UserRole, get_current_user, require_role
from .schemas import RebookBase, RebookResponse
from .services import borrow_book, get_all_rebooks, return_book

rebooks_router = APIRouter(prefix="/rebooks", tags=["Rebooks"])


@rebooks_router.post("/", response_model=RebookResponse)
async def borrow(
    rebook_data: RebookBase,
    db: AsyncSession = Depends(get_async_session),
    current_user=Depends(get_current_user),
):
    return await borrow_book(db, current_user.id, rebook_data.book_id)


@rebooks_router.post("/return", response_model=RebookResponse)
async def return_rebook(
    rebook_data: RebookBase,
    db: AsyncSession = Depends(get_async_session),
    current_user=Depends(get_current_user),
):
    return await return_book(db, current_user.id, rebook_data.book_id)


@rebooks_router.get("/", response_model=list[RebookResponse])
async def list_rebooks(
    db: AsyncSession = Depends(get_async_session),
    current_user=Depends(require_role(UserRole.ADMIN)),
):

    return await get_all_rebooks(db)
