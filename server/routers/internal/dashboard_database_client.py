from sqlmodel import SQLModel, Field, create_engine

from typing import Optional

class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    email: str
    password: str
    is_admin: bool