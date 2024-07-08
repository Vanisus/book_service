from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class Book(BaseModel):
    id: int
    title: str
    author: str
    published_date: Optional[str] = None
    status: Optional[str] = None


class BookCreate(BaseModel):
    title: str
    author: str
    published_date: datetime
    status: str = "available"


class BookUpdate(BaseModel):
    title: str = None
    author: str = None
    published_date: datetime = None
    status: str = None
