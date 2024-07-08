from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class Rental(BaseModel):
    id: int
    user_id: int
    book_id: int
    rental_date: datetime
    return_date: Optional[datetime] = None
    status: str

    class Config:
        orm_mode = True
