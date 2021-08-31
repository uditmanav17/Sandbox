# https://sqlmodel.tiangolo.com/tutorial/fastapi/simple-hero-api/
# https://sqlmodel.tiangolo.com/tutorial/fastapi/response-model/
# https://sqlmodel.tiangolo.com/tutorial/fastapi/multiple-models/ -> models.py
# https://sqlmodel.tiangolo.com/tutorial/fastapi/limit-and-offset/ -> read_heroes
# https://sqlmodel.tiangolo.com/tutorial/fastapi/update/ -> update_hero, models.py -> HeroUpdate
# https://sqlmodel.tiangolo.com/tutorial/fastapi/delete/ -> delete_hero
from typing import List

import uvicorn
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import RedirectResponse
from models import ENGINE, Hero, HeroCreate, HeroRead, HeroUpdate
from sqlmodel import Session, SQLModel, select


def create_db_and_tables():
    SQLModel.metadata.create_all(ENGINE)


app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/", include_in_schema=False)
def docs_redirect():
    return RedirectResponse("/docs")


@app.post(
    "/heroes/",
    response_model=HeroRead,
    # response_model_exclude_unset=True,
    # response_model_exclude={"secret_name"},
)
def create_hero(hero: HeroCreate):
    with Session(ENGINE) as session:
        db_hero = Hero.from_orm(hero)
        session.add(db_hero)
        session.commit()
        session.refresh(db_hero)
        return db_hero


# Let's add limit and offset to the query parameters.
# By default, we will return the first results from the database, so offset will have a default value of 0.
# And by default, we will return a maximum of 100 heroes, so limit will have a default value of 100.
@app.get("/heroes/", response_model=List[HeroRead])
def read_heroes(offset: int = 0, limit: int = Query(default=100, lte=100)):
    with Session(ENGINE) as session:
        heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
        return heroes


@app.get("/heroes/{hero_id}", response_model=HeroRead)
def read_hero(hero_id: int):
    with Session(ENGINE) as session:
        hero = session.get(Hero, hero_id)
        if not hero:
            raise HTTPException(status_code=404, detail="Hero not found")
        return hero


# We will use a PATCH HTTP operation. This is used to partially update data, which is what we are doing.
@app.patch("/heroes/{hero_id}", response_model=HeroRead)
def update_hero(hero_id: int, hero: HeroUpdate):
    with Session(ENGINE) as session:
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


@app.delete("/heroes/{hero_id}")
def delete_hero(hero_id: int):
    with Session(ENGINE) as session:
        hero = session.get(Hero, hero_id)
        if not hero:
            raise HTTPException(status_code=404, detail="Hero not found")
        session.delete(hero)
        session.commit()
        return {"ok": True}


if __name__ == "__main__":
    # file_name:object
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
