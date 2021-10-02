# https://sqlmodel.tiangolo.com/tutorial/fastapi/simple-hero-api/
# https://sqlmodel.tiangolo.com/tutorial/fastapi/response-model/
# https://sqlmodel.tiangolo.com/tutorial/fastapi/multiple-models/ -> models.py
# https://sqlmodel.tiangolo.com/tutorial/fastapi/limit-and-offset/ -> read_heroes
# https://sqlmodel.tiangolo.com/tutorial/fastapi/update/ -> update_hero, models.py -> HeroUpdate
# https://sqlmodel.tiangolo.com/tutorial/fastapi/delete/ -> delete_hero
# https://sqlmodel.tiangolo.com/tutorial/fastapi/session-with-dependency/ -> fastapi sessions -> all funcs updated
# https://sqlmodel.tiangolo.com/tutorial/fastapi/teams/ -> models.py
# https://sqlmodel.tiangolo.com/tutorial/fastapi/relationships/ -> models.py
# fastapi customization -> https://fastapi.tiangolo.com/tutorial/metadata/
# fastapi customization -> https://fastapi.tiangolo.com/tutorial/path-operation-configuration/
# fastapi Auth -> https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
from typing import List

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Query, status
from fastapi.responses import JSONResponse
from hero_auth import auth_router, get_current_active_user
from models import (
    Hero,
    HeroCreate,
    HeroRead,
    HeroReadWithTeam,
    HeroUpdate,
    Team,
    TeamCreate,
    TeamRead,
    TeamReadWithHeroes,
    TeamUpdate,
    User,
)
from sqlmodel import Session, SQLModel, select, create_engine
from starlette.responses import HTMLResponse
import os
import socket
from pathlib import Path


def create_db_and_tables():
    try:
        DB_SERVICE_PORT = os.environ.get("DB_SERVICE_PORT")
        DB_SERVICE_NAME = os.environ.get("DB_SERVICE_NAME")
        POSTGRES_DB = os.environ.get("POSTGRES_DB")
        DB_USERNAME = os.environ.get("POSTGRES_USER")
        DB_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
        # DB_URI = "postgresql://udit:uditmanav@postgres:5432/ud_db"
        DB_URI = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_SERVICE_NAME}:{DB_SERVICE_PORT}/{POSTGRES_DB}"
        ENGINE = create_engine(DB_URI, echo=True)
        SQLModel.metadata.create_all(ENGINE)
    except:
        print("CAN'T CONNECT TO POSTGRESQL\n\tFALLING BACK TO SQLITE")
        SQLITE_FILE_NAME = Path("./sql-db/database.db")
        SQLITE_FILE_NAME.parent.mkdir(parents=True, exist_ok=True)
        SQLITE_DB_URI = f"sqlite:///{SQLITE_FILE_NAME}"
        connect_args = {"check_same_thread": False}
        ENGINE = create_engine(SQLITE_DB_URI, echo=True, connect_args=connect_args)
        SQLModel.metadata.create_all(ENGINE)
    return ENGINE


def create_teams_and_heroes():
    with Session(ENGINE) as session:
        # creating teams
        team_preventers = Team(name="Preventers", headquarters="Sharp Tower")
        team_z_force = Team(name="Z-Force", headquarters="Sister Margaret’s Bar")
        session.add(team_preventers)
        session.add(team_z_force)
        session.commit()

        # creating heroes and assigning them to team
        hero_deadpond = Hero(
            name="Deadpond", secret_name="Dive Wilson", team_id=team_z_force.id
        )
        hero_rusty_man = Hero(
            name="Rusty-Man",
            secret_name="Tommy Sharp",
            age=48,
            team_id=team_preventers.id,
        )
        hero_spider_boy = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")
        session.add(hero_deadpond)
        session.add(hero_rusty_man)
        session.add(hero_spider_boy)
        session.commit()


def add_dummy_data():
    with Session(ENGINE) as session:
        # check if heroes/teams are present in DB
        heroes_count = len(session.exec(select(Hero.id)).all())
        teams_count = len(session.exec(select(Team.id)).all())

    print(heroes_count, teams_count)
    if heroes_count == 0 and teams_count == 0:
        create_teams_and_heroes()


description = f"""
Heroes and Teams API helps you do awesome stuff. 🚀
Served by Container with ID - **{socket.gethostname()}**

## Heroes
You can **create, read and update heroes**.

## Teams
You will be able to:
* **Create teams** (_implemented_).
* **Read teams** (_implemented_).
* **Update teams** (_implemented_).

## Authorization
You can use any username and password combination for authorization. To check for disabled user use - username:"johndoe", password:"secret" combination.
\nFor example: if username = abc, then password = abc@123.
"""

# The order of each tag metadata dictionary also defines the order shown in the docs UI.
tags_metadata = [
    {
        "name": "teams",
        "description": "Manage teams. So _fancy_ they have their own docs.",
        "externalDocs": {
            "description": "Teams external docs",
            "url": "https://en.wikipedia.org/wiki/Category:Marvel_Comics_superhero_teams",
        },
    },
    {"name": "heroes", "description": "Operations with **heroes**.",},
]
app = FastAPI(
    title="Heroes App",
    description=description,
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Udit Manav",
        "url": "https://github.com/uditmanav17",
        "email": "abc@def.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    openapi_tags=tags_metadata,
    # docs and redoc URL
    docs_url="/documentation",
    # redoc_url="/redoc",
)
app.include_router(auth_router)


@app.on_event("startup")
def on_startup():
    global ENGINE
    ENGINE = create_db_and_tables()
    add_dummy_data()


def get_session():
    with Session(ENGINE) as session:
        yield session


@app.get("/", include_in_schema=False)
def index():
    content = """
        <html>
        <body>
        <title> Heroes App </title>
        <h1>Heroes and Teams management</h1>
        <ul>
            <li><a href='/documentation'> Try API </a></li>
            <li><a href='/redoc'> Documentation </a></li>
        </ul>
        </body>
        </html>
    """
    return HTMLResponse(content=content)


@app.post(
    "/heroes/",
    response_model=HeroRead,
    tags=["heroes"],
    status_code=status.HTTP_201_CREATED,
    # response_model_exclude_unset=True,
    # response_model_exclude={"secret_name"},
)
def create_hero(
    *,
    session: Session = Depends(get_session),
    hero: HeroCreate,
    current_user: User = Depends(get_current_active_user),
):
    # Here we are passing the parameter session that has a "default value" of Depends(get_session)
    # before the parameter hero, that doesn't have any default value.
    # Python would normally complain about that, but we can use the initial "parameter" *,
    # to mark all the rest of the parameters as "keyword only", which solves the problem.
    db_hero = Hero.from_orm(hero)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero


# Let's add limit and offset to the query parameters.
# By default, we will return the first results from the database, so offset will have a default value of 0.
# And by default, we will return a maximum of 100 heroes, so limit will have a default value of 100.
@app.get(
    "/heroes/", response_model=List[HeroRead], tags=["heroes"],
)
def read_heroes(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
):
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes


@app.get(
    "/heroes/{hero_id}", response_model=HeroReadWithTeam, tags=["heroes"],
)
def read_hero(*, session: Session = Depends(get_session), hero_id: int):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero


# We will use a PATCH HTTP operation. This is used to partially update data, which is what we are doing.
@app.patch("/heroes/{hero_id}", response_model=HeroRead, tags=["heroes"])
def update_hero(
    *,
    session: Session = Depends(get_session),
    hero_id: int,
    hero: HeroUpdate,
    current_user: User = Depends(get_current_active_user),
):
    db_hero = session.get(Hero, hero_id)
    if not db_hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    # The HeroUpdate model has all the fields with default values, because they all have defaults,
    # they are all optional, which is what we want.
    # But that also means that if we just call hero.dict() we will get a dictionary
    # that could potentially have several or all of those values with their defaults
    hero_data = hero.dict(exclude_unset=True)
    # And then if we update the hero in the database with this data, we would be removing any existing values,
    # and that's probably not what the client intended.
    # But fortunately Pydantic models (and so SQLModel models) have a parameter
    # we can pass to the .dict() method for that: exclude_unset=True.
    # This tells Pydantic to not include the values that were not sent by the client.
    # Saying it another way, it would only include the values that were sent by the client.
    for key, value in hero_data.items():
        setattr(db_hero, key, value)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero


@app.delete("/heroes/{hero_id}", tags=["heroes"], status_code=status.HTTP_200_OK)
def delete_hero(
    *,
    session: Session = Depends(get_session),
    hero_id: int,
    current_user: User = Depends(get_current_active_user),
):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(hero)
    session.commit()
    return {"ok": True}


@app.post(
    "/teams/",
    response_model=TeamRead,
    tags=["teams"],
    status_code=status.HTTP_201_CREATED,
)
def create_team(
    *,
    session: Session = Depends(get_session),
    team: TeamCreate,
    current_user: User = Depends(get_current_active_user),
):
    db_team = Team.from_orm(team)
    session.add(db_team)
    session.commit()
    session.refresh(db_team)
    return db_team


@app.get(
    "/teams/", response_model=List[TeamRead], tags=["teams"],
)
def read_teams(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
):
    teams = session.exec(select(Team).offset(offset).limit(limit)).all()
    return teams


@app.get(
    "/teams/{team_id}", response_model=TeamReadWithHeroes, tags=["teams"],
)
def read_team(*, team_id: int, session: Session = Depends(get_session)):
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team


@app.patch(
    "/teams/{team_id}", response_model=TeamRead, tags=["teams"],
)
def update_team(
    *,
    session: Session = Depends(get_session),
    team_id: int,
    team: TeamUpdate,
    current_user: User = Depends(get_current_active_user),
):
    db_team = session.get(Team, team_id)
    if not db_team:
        raise HTTPException(status_code=404, detail="Team not found")
    team_data = team.dict(exclude_unset=True)
    for key, value in team_data.items():
        setattr(db_team, key, value)
    session.add(db_team)
    session.commit()
    session.refresh(db_team)
    return db_team


@app.delete("/teams/{team_id}", tags=["teams"], status_code=status.HTTP_200_OK)
def delete_team(
    *,
    session: Session = Depends(get_session),
    team_id: int,
    current_user: User = Depends(get_current_active_user),
):
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    session.delete(team)
    session.commit()
    return {"ok": True}


if __name__ == "__main__":
    # to run from cli use - uvicorn app:app --reload
    # file_name:object
    port = os.environ.get("APPLICATION_PORT", 8081)
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=True)
