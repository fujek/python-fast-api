from typing import Optional

from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime


class BorrowInput(SQLModel):
    book_id: int = Field(foreign_key="book.id")


class Borrow(BorrowInput, table=True):
    id: int = Field(default=None, primary_key=True)
    book: "Book" = Relationship(back_populates="borrowing")
    user_id: int = Field(foreign_key="user.id")
    borrow_date: datetime = Field(default=datetime.utcnow())
    return_date: Optional[datetime] = Field(default=None)

