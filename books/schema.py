from typing import Optional

from sqlmodel import SQLModel, Field, Relationship

from author.schema import Author


class BookInput(SQLModel):
    name: str
    isbn: str
    author_id: int = Field(foreign_key="author.id")
    description: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "W pustyni i w puszczy",
                    "isbn": "1212103-2321-11",
                    "author_id": 1,
                    "description": "Book's short description"
                }
            ]
        }
    }


class Book(BookInput, table=True):
    id: int = Field(default=None, primary_key=True)
    cover_file_name: Optional[str] = None
    author: Author = Relationship(back_populates="books")
