from datetime import datetime

from pydantic import BaseModel, ConfigDict


class RebookBase(BaseModel):
    book_id: int


class RebookResponse(RebookBase):
    id: int
    borrowed_at: datetime
    due_date: datetime
    returned_at: datetime | None
    user_id: int

    model_config = ConfigDict(from_attributes=True)
