from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from db import init_db
from schemas import Book, BookCreate, BookUpdate
from crud import get_all_book_from_db, get_book, update_book_data, delete_book_from_db, create_book
import requests
import logging
from datetime import datetime
from settings import settings
import requests

app = FastAPI(
    title="Book service"
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

FILE_SERVICE_URL = settings.file_service_url


@app.on_event("startup")
async def on_startup():
    await init_db()


@app.post('/books/', response_model=Book, tags=['Books'])
async def add_book(
        title: str = Form(...),
        author: str = Form(...),
        status: str = Form(...),
        file: UploadFile = File(...)
):
    book_data = BookCreate(title=title, author=author, published_date=datetime.utcnow(), status=status).dict()

    files = {"file": (file.filename, file.file, file.content_type)}
    file_response = requests.post(f"{FILE_SERVICE_URL}/files/upload", files=files)
    if file_response.status_code != 200:
        raise HTTPException(status_code=file_response.status_code, detail="File upload failed")
    file_data = file_response.json()
    book_data["book_path"] = file_data["file_path"]
    return await create_book(book_data)


@app.get('/books/', response_model=Book, tags=['Books'])
async def get_all_books():
    return await get_all_book_from_db()


@app.get('/books/{book_id}', response_model=Book, tags=['Books'])
async def get_book_by_id(book_id: int):
    return await get_book(book_id)


@app.put('/books/{book_id}', response_model=BookUpdate, tags=['Books'])
async def update_book(book_id: int, book_data: BookUpdate):
    updated_book = await update_book_data(book_id, book_data.dict(exclude_unset=True))
    return updated_book


@app.delete('/books/{book_id}', response_model=Book, tags=['Books'])
async def delete_book(book_id: int):
    return await delete_book_from_db(book_id)
