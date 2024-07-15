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

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "user_id": 1,
                "book_id": 1,
                "rental_date": datetime.utcnow(),
                "return_date": None,
                "status": "rented"
            }
        }
    }
