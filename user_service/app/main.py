from fastapi import FastAPI
from base_config import auth_backend, fastapi_users
from schemas import UserRead, UserCreate
from crud import update_user, get_user, delete_user
from db import init_db

app = FastAPI(
    title="User service",
    description="API documentation for User Service.",
    version="1.0.0",
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/user",
    tags=["User"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/user",
    tags=["User"],
)


@app.on_event("startup")
async def on_startup():
    await init_db()


@app.get('/users/{user_id}', response_model=UserRead, tags=['User'])
async def get_user_with_id(user_id: int):
    return await get_user(user_id)


@app.put('/users/{user_id}', response_model=UserRead, tags=['User'])
async def update_user_with_id(user_id: int, user_update: UserCreate):
    user_update_data = user_update.dict(exclude_unset=True)
    return await update_user(user_id, user_update_data)


@app.delete("/users/{user_id}", tags=['User'])
async def delete_user_with_id(user_id: int):
    return await delete_user(user_id)
