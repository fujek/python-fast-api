from pydantic import BaseModel
from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
