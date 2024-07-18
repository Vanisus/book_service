from fastapi import FastAPI, Form, HTTPException
from crud import get_rental_by_user, get_rental_by_book, return_rental, create_rental, get_rental_by_user_and_book
from schemas import Rental
from db import init_db
import requests
from settings import settings

app = FastAPI(
    title="Rental service"
)

BOOK_SERVICE_URL = settings.book_service_url


@app.on_event("startup")
async def on_startup():
    await init_db()


@app.post('/rental/', response_model=Rental, tags=['Rental'])
async def rent_book(user_id: int = Form(...), book_id: int = Form(...)):
    existing_rental = await get_rental_by_user_id_and_book_id(user_id, book_id)
    if not existing_rental or existing_rental[0].status == "returned":
        book_response = requests.get(f"{BOOK_SERVICE_URL}/books/{book_id}")
        if book_response.json()["status"] == "rented":
            raise HTTPException(status_code=book_response.status_code, detail="Book is already rented")
        update_response = requests.put(f"{BOOK_SERVICE_URL}/books/{book_id}", json={"status": "rented"})
        if update_response.status_code != 200:
            raise HTTPException(status_code=update_response.status_code, detail="Failed to update book status")

        return await create_rental(user_id, book_id)
    raise HTTPException(status_code=404, detail="This book is not available for rent")


@app.post("/rental/return/{rental_id}", response_model=Rental, tags=['Rental'])
async def return_book(rental_id: int):
    return_response = await return_rental(rental_id)
    if return_response.status == "returned":
        book_response = requests.put(f"{BOOK_SERVICE_URL}/books/{return_response.book_id}", json={"status": "available"})
        if book_response.status_code != 200:
            raise HTTPException(status_code=book_response.status_code, detail="Failed to update book status")
    return return_response


@app.get("/rental/user/{user_id}", response_model=Rental, tags=['Rental'])
async def get_rental_by_user_id(user_id: int):
    return await get_rental_by_user(user_id)


@app.get("/rental/books/{book_id}", tags=['Rental'])
async def get_rental_by_book_id(book_id: int):
    return await get_rental_by_book(book_id)


@app.get("/rental/", tags=['Rental'])
async def get_rental_by_user_id_and_book_id(user_id: int, book_id: int):
    return await get_rental_by_user_and_book(book_id, user_id)