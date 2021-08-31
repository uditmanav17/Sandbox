from typing import Optional

from sqlmodel import Field, SQLModel, create_engine

SQLITE_FILE_NAME = "database.db"
SQLITE_URL = f"sqlite:///{SQLITE_FILE_NAME}"

connect_args = {"check_same_thread": False}
ENGINE = create_engine(SQLITE_URL, echo=True, connect_args=connect_args)


class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: Optional[int] = None
