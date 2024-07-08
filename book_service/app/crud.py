from fastapi import HTTPException
from sqlalchemy import select
from db import get_async_session
from models import BookSQL


async def create_book(book_data: dict) -> BookSQL:
    async with get_async_session() as session:
        book = BookSQL(**book_data)
        session.add(book)
        await session.commit()
        await session.refresh(book)
        return book


async def get_book(book_id: int) -> BookSQL:
    async with get_async_session() as session:
        book = await session.get(BookSQL, book_id)
        if book is None:
            raise HTTPException(status_code=404, detail="Book not found")
        return book


async def update_book_data(book_id: int, book_data: dict) -> BookSQL:
    async with get_async_session() as session:
        book = await session.get(BookSQL, book_id)
        for key, value in book_data.items():
            setattr(book, key, value)
        session.add(book)
        await session.commit()
        await session.refresh(book)
        return book


async def delete_book_from_db(book_id: int):
    async with get_async_session() as session:
        book = await session.get(BookSQL, book_id)
        await session.delete(book)
        await session.commit()
        return {"message": f"Book with id={book.id} was deleted"}


async def get_all_book_from_db():
    async with get_async_session() as session:
        result = await session.execute(
            select(BookSQL)
        )
        return result.scalars().all()
