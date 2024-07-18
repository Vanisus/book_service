from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class Book(BaseModel):
    id: int
    title: str
    author: str
    published_date: Optional[datetime] = None
    status: Optional[str] = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "title": "Sample book title",
                "author": "Sample Author",
                "published_date": "2021-01-01",
                "status": "available"
            }
        }
    }


class BookCreate(BaseModel):
    title: str
    author: str
    published_date: datetime
    status: str = "available"

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Sample book title",
                "author": "Sample Author",
                "published_date": "2021-01-01",
                "status": "available"
            }
        }
    }


class BookUpdate(BaseModel):
    title: str = None
    author: str = None
    published_date: datetime = None
    status: str = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Sample book title",
                "author": "Sample Author",
                "published_date": "2021-01-01",
                "status": "rented"
            }
        }
    }
