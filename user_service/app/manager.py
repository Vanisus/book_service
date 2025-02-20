from typing import Optional
from fastapi import Depends, Request
from fastapi_users import BaseUserManager, schemas, models, exceptions
from models import User
from crud import get_user_db
from settings import settings


class UserManager(BaseUserManager[User, int]):
    reset_password_token_secret = settings.secret_auth_key
    verification_token_secret = settings.secret_auth_key

    def __init__(self, user_db):
        super().__init__(user_db)
        self.user_db = user_db

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def create(
            self,
            user_create: schemas.UC,
            safe: bool = False,
            request: Optional[Request] = None,
    ) -> models.UP:
        await self.validate_password(user_create.password, user_create)

        async for user_db in get_user_db():
            existing_user = await user_db.get_by_email(user_create.email)
            if existing_user is not None:
                raise exceptions.UserAlreadyExists()

            user_dict = (
                user_create.create_update_dict()
                if safe
                else user_create.create_update_dict_superuser()
            )
            password = user_dict.pop("password")
            user_dict["hashed_password"] = self.password_helper.hash(password)

            created_user = await user_db.create(user_dict)

            await self.on_after_register(created_user, request)

            return created_user

    def parse_id(self, user_id: str) -> int:
        try:
            return int(user_id)
        except ValueError:
            raise exceptions.UserNotExists()


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
