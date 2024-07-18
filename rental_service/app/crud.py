from datetime import datetime
from fastapi import HTTPException
from sqlalchemy import select
from models import Rental
from db import get_async_session


async def create_rental(user_id: int, book_id: int) -> Rental:
    async with get_async_session() as session:
        rental = Rental(user_id=user_id, book_id=book_id)
        session.add(rental)
        await session.commit()
        await session.refresh(rental)
        return rental


async def return_rental(rental_id: int) -> Rental:
    async with get_async_session() as session:
        rental = await session.get(Rental, rental_id)
        if rental is None:
            raise HTTPException(status_code=404, detail="Rental not found")
        rental.return_date = datetime.utcnow()
        rental.status = "returned"
        await session.commit()
        await session.refresh(rental)
        return rental


async def get_rental_by_user(user_id: int):
    async with get_async_session() as session:
        result = await session.execute(
            select(Rental)
            .where(Rental.user_id == user_id)
        )
        return result.scalars().all()


async def get_rental_by_book(book_id: int):
    async with get_async_session() as session:
        result = await session.execute(
            select(Rental)
            .where(Rental.book_id == book_id)
        )
        return result.scalars().all()


async def get_rental_by_user_and_book(book_id: int, user_id: int):
    async with get_async_session() as session:
        result = await session.execute(
            select(Rental)
            .where(Rental.book_id == book_id, Rental.user_id == user_id)
        )
        return result.scalars().all()
