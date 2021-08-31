# https://sqlmodel.tiangolo.com/tutorial/fastapi/simple-hero-api/

import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from models import ENGINE, Hero
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


@app.post("/heroes/")
def create_hero(hero: Hero):
    with Session(ENGINE) as session:
        session.add(hero)
        session.commit()
        session.refresh(hero)
        return hero


@app.get("/heroes/")
def read_heroes():
    with Session(ENGINE) as session:
        heroes = session.exec(select(Hero)).all()
        return heroes


if __name__ == "__main__":
    # file_name:object
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
