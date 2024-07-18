from datetime import datetime
from sqlalchemy import Index
from sqlalchemy.orm import Mapped, mapped_column
from db import Base


class BookSQL(Base):
    __tablename__ = 'book'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(nullable=False)
    author: Mapped[str] = mapped_column(nullable=False)
    published_date: Mapped[datetime]
    book_path: Mapped[str] = mapped_column(nullable=True)
    status: Mapped[str] = mapped_column(default="available")

    __table_args__ = (
        Index("ix_book_title", "title"),
        Index('ix_book_author', "author")
    )

