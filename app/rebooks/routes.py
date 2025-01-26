from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_async_session
from ..users import get_current_user
from .schemas import RebookCreate, RebookResponse
from .services import borrow_book, return_book

rebooks_router = APIRouter(prefix="/rebooks", tags=["Rebooks"])


@rebooks_router.post("/", response_model=RebookResponse)
async def borrow(
    rebook_data: RebookCreate,
    db: AsyncSession = Depends(get_async_session),
    current_user=Depends(get_current_user),
):
    return await borrow_book(db, current_user.id, rebook_data.book_id)


@rebooks_router.post("/{rebook_id}/return", response_model=RebookResponse)
async def return_rebook(
    rebook_data: RebookCreate,
    db: AsyncSession = Depends(get_async_session),
    current_user=Depends(get_current_user),
):
    return await return_book(db, current_user.id, rebook_data.book_id)


# @rebooks_router.get("/", status_code=status.HTTP_200_OK)
# def list_rebooks(
#     db: AsyncSession = Depends(get_async_session),
#     current_user=Depends(get_current_user),
# ):
#     if current_user.role != "admin":
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Only admins can view all borrowings.",
#         )

#     rebooks = db.query(Rebook).all()
#     return rebooks
