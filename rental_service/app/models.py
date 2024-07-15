from datetime import datetime
from sqlalchemy import ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column
from db import Base


class Rental(Base):
    __tablename__ = 'rental'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(nullable=False, index=True)
    book_id: Mapped[int] = mapped_column(nullable=False, index=True)
    rental_date: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    return_date: Mapped[datetime] = mapped_column(nullable=True)
    status: Mapped[str] = mapped_column(default="rented")

    __table_args__ = (
        Index('ix_rental_user_id_book_id', 'user_id', 'book_id'),
    )
