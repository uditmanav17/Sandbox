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
from typing import List

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Query, status
from fastapi.responses import JSONResponse
from models import (
    ENGINE,
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
)
from sqlmodel import Session, SQLModel, select
from starlette.responses import HTMLResponse


def create_db_and_tables():
    SQLModel.metadata.create_all(ENGINE)


description = """
Heroes and Teams API helps you do awesome stuff. 🚀

## Heroes

You can **create, read and update heroes**.

## Teams

You will be able to:

* **Create teams** (_implemented_).
* **Read teams** (_implemented_).
* **Update teams** (_implemented_).
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
    {
        "name": "heroes",
        "description": "Operations with **heroes**.",
    },
]
app = FastAPI(
    title="Heroes App",
    description=description,
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Udit Manav",
        "url": "https://www.google.com/",
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


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


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
def create_hero(*, session: Session = Depends(get_session), hero: HeroCreate):
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
    "/heroes/",
    response_model=List[HeroRead],
    tags=["heroes"],
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
    "/heroes/{hero_id}",
    response_model=HeroReadWithTeam,
    tags=["heroes"],
)
def read_hero(*, session: Session = Depends(get_session), hero_id: int):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero


# We will use a PATCH HTTP operation. This is used to partially update data, which is what we are doing.
@app.patch("/heroes/{hero_id}", response_model=HeroRead, tags=["heroes"])
def update_hero(
    *, session: Session = Depends(get_session), hero_id: int, hero: HeroUpdate
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
def delete_hero(*, session: Session = Depends(get_session), hero_id: int):
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
def create_team(*, session: Session = Depends(get_session), team: TeamCreate):
    db_team = Team.from_orm(team)
    session.add(db_team)
    session.commit()
    session.refresh(db_team)
    return db_team


@app.get(
    "/teams/",
    response_model=List[TeamRead],
    tags=["teams"],
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
    "/teams/{team_id}",
    response_model=TeamReadWithHeroes,
    tags=["teams"],
)
def read_team(*, team_id: int, session: Session = Depends(get_session)):
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team


@app.patch(
    "/teams/{team_id}",
    response_model=TeamRead,
    tags=["teams"],
)
def update_team(
    *,
    session: Session = Depends(get_session),
    team_id: int,
    team: TeamUpdate,
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
def delete_team(*, session: Session = Depends(get_session), team_id: int):
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    session.delete(team)
    session.commit()
    return {"ok": True}


if __name__ == "__main__":
    # to run from cli use - uvicorn app:app --reload
    # file_name:object
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
