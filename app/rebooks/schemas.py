from datetime import datetime

from pydantic import BaseModel


class RebookBase(BaseModel):
    book_id: int


class RebookResponse(RebookBase):
    id: int
    borrowed_at: datetime
    due_date: datetime
    returned_at: datetime | None
    user_id: int

    class Config:
        from_attributes = True
