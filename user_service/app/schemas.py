from typing import Optional
from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    id: int
    email: str
    username: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "email": "user@example.com",
                "username": "user123",
                "is_active": True,
                "is_superuser": False,
                "is_verified": False

            }
        }
    }


class UserCreate(schemas.BaseUserCreate):
    username: str
    email: str
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "user@example.com",
                "username": "user123",
                "password": "password",
                "is_active": True,
                "is_superuser": False,
                "is_verified": False
            }
        }
    }
