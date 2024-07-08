from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from base_config import auth_backend, fastapi_users
from schemas import UserRead, UserCreate
from crud import get_async_session, update_user, get_user, delete_user
from models import User
from manager import get_user_manager
app = FastAPI(
    title="User service"
)


app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)


@app.get('/users/{id}', response_model=UserRead)
async def get_user_with_id(user_id: int):
    return await get_user(user_id)


@app.put('/users/{id}', response_model=UserRead)
async def update_user_with_id(user_id: int, user_update: UserCreate):
    user_update_data = user_update.dict(exclude_unset=True)
    return await update_user(user_id, user_update_data)


@app.delete("/users/{id}")
async def delete_user_with_id(user_id: int):
    return await delete_user(user_id)
