from typing import Optional

from sqlmodel import Field
from sqlmodel import SQLModel


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    username: str = Field(unique=True, index=True)
    first_name: str
    last_name: str
    hashed_password: str
    role: str
    is_active: bool = Field(default=True)
    phone_number: str
