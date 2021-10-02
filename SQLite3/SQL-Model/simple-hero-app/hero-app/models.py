from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel, create_engine
import os

# SQLITE_FILE_NAME = "database.db"
# DB_URI = f"sqlite:///{SQLITE_FILE_NAME}"
# DB_URI = "postgresql://udit:uditmanav@postgres:5432/ud_db"
DB_SERVICE_PORT = os.environ.get("DB_SERVICE_PORT")
DB_SERVICE_NAME = os.environ.get("DB_SERVICE_NAME")
POSTGRES_DB = os.environ.get("POSTGRES_DB")
DB_USERNAME = os.environ.get("POSTGRES_USER")
DB_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
DB_URI = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_SERVICE_NAME}:{DB_SERVICE_PORT}/{POSTGRES_DB}"

connect_args = {"check_same_thread": False}
# ENGINE = create_engine(DB_URI, echo=True, connect_args=connect_args)
ENGINE = create_engine(DB_URI, echo=True)


class TeamBase(SQLModel):
    name: str
    headquarters: str


class Team(TeamBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    heroes: List["Hero"] = Relationship(back_populates="team")


class TeamCreate(TeamBase):
    pass


class TeamRead(TeamBase):
    id: int


class TeamUpdate(SQLModel):
    id: Optional[int] = None
    name: Optional[str] = None
    headquarters: Optional[str] = None


class HeroBase(SQLModel):
    name: str
    secret_name: str
    age: Optional[int] = None

    team_id: Optional[int] = Field(default=None, foreign_key="team.id")


class Hero(HeroBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    team: Optional[Team] = Relationship(back_populates="heroes")


class HeroRead(HeroBase):
    id: int


class HeroCreate(HeroBase):
    pass


class HeroUpdate(SQLModel):
    name: Optional[str] = None
    secret_name: Optional[str] = None
    age: Optional[int] = None
    team_id: Optional[int] = None


# Inheritance and Type Annotations
# The HeroReadWithTeam inherits from HeroRead, which means that
# it will have the normal fields for reading, including the required id that was declared in HeroRead.
# And then it adds the new field team, which could be None, and is declared
# with the type TeamRead with the base fields for reading a team.
class HeroReadWithTeam(HeroRead):
    team: Optional[TeamRead] = None


class TeamReadWithHeroes(TeamRead):
    heroes: List[HeroRead] = []


# models used for authorization
class Token(SQLModel):
    access_token: str
    token_type: str


class TokenData(SQLModel):
    username: Optional[str] = None


class User(SQLModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(User):
    hashed_password: str
