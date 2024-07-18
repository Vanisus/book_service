from fastapi import HTTPException
from sqlalchemy import select
from db import get_async_session
from models import File
import os
from settings import settings

UPLOAD_DIRECTORY = settings.upload_directory


async def upload_file(file_data: dict) -> File:
    async with get_async_session() as session:
        file = File(**file_data)
        session.add(file)
        await session.commit()
        await session.refresh(file)
        return file


async def get_file(filename: str):
    async with get_async_session() as session:
        result = await session.execute(
            select(File)
            .where(File.filename == filename)
        )
        file = result.scalars().first()
        if file is None:
            raise HTTPException(status_code=404, detail="File not found")
        return file


async def delete_file(filename: str):
    file = await get_file(filename)
    file_path = file.file_path
    if os.path.exists(file_path):
        os.remove(file_path)
    async with get_async_session() as session:
        await session.delete(file)
        await session.commit()
        return {"message": f"File {filename} was deleted"}
