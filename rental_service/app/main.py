from fastapi import FastAPI
from crud import get_rental_by_user, get_rental_by_book, return_rental, create_rental
from schemas import Rental

app = FastAPI(
    title="Rental service"
)


@app.post('/rental/', response_model=Rental)
async def rent_book(user_id: int, book_id: int):
    return await create_rental(user_id, book_id)


@app.post("/rental/return/{id}", response_model=Rental)
async def return_book(book_id: int):
    return await return_rental(book_id)


@app.get("/rental/user/{id}", response_model=Rental)
async def get_rental_by_user_id(user_id: int):
    return await get_rental_by_user(user_id)


@app.get("/rental/books/{id}")
async def get_rental_by_book_id(book_id: int):
    return await get_rental_by_book(book_id)

