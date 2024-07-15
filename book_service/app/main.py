from fastapi import FastAPI, UploadFile, File, HTTPException
from db import init_db
from schemas import Book, BookCreate, BookUpdate
from crud import get_all_book_from_db, get_book, update_book_data, delete_book_from_db, create_book
import requests
from settings import settings

app = FastAPI(
    title="Book service"
)

FILE_SERVICE_URL = settings.file_service_url


@app.on_event("startup")
async def on_startup():
    await init_db()


@app.post('/books/', response_model=Book, tags=['Books'])
async def add_book(book_data: BookCreate, file: UploadFile = File(...)):
    file_response = requests.post(f"{FILE_SERVICE_URL}/files/upload", files={"file": file.file})
    if file_response.status_code != 200:
        raise HTTPException(status_code=file_response.status_code, detail="File upload failed")
    file_data = file_response.json()
    book_data.book_path = file_data["file_path"]
    return await create_book(book_data.dict())


@app.get('/books/', response_model=Book, tags=['Books'])
async def get_all_books():
    return await get_all_book_from_db()


@app.get('/books/{id}', response_model=Book, tags=['Books'])
async def get_book_by_id(book_id: int):
    return await get_book(book_id)


@app.put('/books/', response_model=Book, tags=['Books'])
async def update_book(book_data: BookUpdate, book_id: int):
    return await update_book_data(book_id, book_data.dict(exclude_unset=True))


@app.delete('/books/{id}', response_model=Book, tags=['Books'])
async def delete_book(book_id: int):
    return await delete_book_from_db(book_id)
