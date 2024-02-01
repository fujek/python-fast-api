from sqlmodel import SQLModel, Field, Relationship

from author.schema import Author


class BookInput(SQLModel):
    name: str
    isbn: str
    cover: str
    author_id: int = Field(foreign_key="author.id")


class Book(BookInput, table=True):
    id: int = Field(default=None, primary_key=True)
    author: Author = Relationship(back_populates="books")