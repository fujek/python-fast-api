from datetime import datetime
from enum import Enum

from pydantic import BaseModel
from sqlmodel import SQLModel, Field


class UserRole(str, Enum):
    ADMIN = "ADMIN"
    USER = "USER"


class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str
    password: str
    role: UserRole


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenUser(BaseModel):
    sub: str
    user_id: int
    exp: datetime
    role: UserRole
