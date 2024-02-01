
from sqlmodel import SQLModel, Field, Relationship


class AuthorInput(SQLModel):
    name: str


class Author(AuthorInput, table=True):
    id: int = Field(default=None, primary_key=True)
    books: list["Book"] = Relationship(back_populates="author")


class BookInput(SQLModel):
    name: str
    isbn: str
    cover: str
    author_id: int = Field(foreign_key="author.id")


class Book(BookInput, table=True):
    id: int = Field(default=None, primary_key=True)
    author: Author = Relationship(back_populates="books")
