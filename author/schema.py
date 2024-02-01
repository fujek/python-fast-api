
from sqlmodel import SQLModel, Field, Relationship


class AuthorInput(SQLModel):
    name: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Henryk Sienkiewicz"
                }
            ]
        }
    }


class Author(AuthorInput, table=True):
    id: int = Field(default=None, primary_key=True)
    books: list["Book"] = Relationship(back_populates="author")