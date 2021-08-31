# https://sqlmodel.tiangolo.com/tutorial/fastapi/simple-hero-api/
# https://sqlmodel.tiangolo.com/tutorial/fastapi/response-model/
# https://sqlmodel.tiangolo.com/tutorial/fastapi/multiple-models/ -> models.py

from typing import List

import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from models import ENGINE, Hero, HeroCreate, HeroRead
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


@app.get("/heroes/", response_model=List[HeroRead])
def read_heroes():
    with Session(ENGINE) as session:
        heroes = session.exec(select(Hero)).all()
        return heroes


if __name__ == "__main__":
    # file_name:object
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
