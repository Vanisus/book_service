from fastapi import Depends, HTTPException
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession
from models import User
from db import get_async_session
from contextlib import contextmanager, asynccontextmanager


async def get_user_db() -> SQLAlchemyUserDatabase:
    async with get_async_session() as session:
        yield SQLAlchemyUserDatabase(session, User)


async def get_user(user_id: int) -> User:
    async with get_async_session() as session:
        user = await session.get(User, user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user


async def update_user(user_id: int, user_update: dict) -> User:
    async with get_async_session() as session:
        user = await get_user(user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        for key, value in user_update.items():
            setattr(user, key, value)

        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user


async def delete_user(user_id: int):
    async with get_async_session() as session:
        user = await get_user(user_id)

        await session.delete(user)
        await session.commit()
        return {"message": f"user with id ={user.id} was deleted"}
