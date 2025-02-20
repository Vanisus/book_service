import os.path
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from settings import settings
from crud import upload_file, delete_file, get_file
from db import init_db
from schemas import FileResponse

app = FastAPI(
    title="File service"
)

UPLOAD_DIRECTORY = settings.upload_directory


@app.on_event("startup")
async def on_startup():
    await init_db()
    if not os.path.exists(UPLOAD_DIRECTORY):
        os.makedirs(UPLOAD_DIRECTORY)


@app.post("/files/upload", response_model=FileResponse, tags=['File'])
async def upload_file_endpoint(file: UploadFile = File(...)):
    file_location = os.path.join(UPLOAD_DIRECTORY, file.filename)

    if os.path.exists(file_location):
        raise HTTPException(status_code=409, detail="File already exists")

    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    file_data = {
        "filename": file.filename,
        "file_path": file_location
    }
    return await upload_file(file_data)


@app.get("/files/{filename}", tags=['File'])
async def get_file_endpoint(filename: str):
    return await get_file(filename)


@app.delete("/files/{filename}", tags=['File'])
async def delete_file_endpoint(filename: str):
    return await delete_file(filename)



