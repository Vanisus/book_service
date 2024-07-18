from pydantic import BaseModel


class FileResponse(BaseModel):
    filename: str
    file_path: str
