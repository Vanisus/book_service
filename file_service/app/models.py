from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from db import Base


class File(Base):
    __tablename__ = 'file'

    id: Mapped[int] = mapped_column(primary_key=True)
    filename: Mapped[str] = mapped_column(nullable=False, unique=True)
    file_path: Mapped[str] = mapped_column(nullable=False, unique=True)
    uploaded_at: Mapped[datetime] = mapped_column(default=datetime.utcnow())

