from fastapi_users import FastAPIUsers
from fastapi_users.authentication import (AuthenticationBackend,
                                          CookieTransport, JWTStrategy)

from manager import get_user_manager
from models import User
from settings import settings

cookie_transport = CookieTransport(cookie_name="user_auth", cookie_max_age=3600)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.secret_auth_key, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()