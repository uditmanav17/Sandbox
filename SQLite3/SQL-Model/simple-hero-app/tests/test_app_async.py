# https://sqlmodel.tiangolo.com/tutorial/fastapi/tests/

import pytest
from app import app, get_session

# from fastapi.testclient import TestClient
from httpx import AsyncClient
from models import Hero
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from starlette import responses


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://",  # using in-memory db
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
        # we use an in-memory database, we need to also tell SQLAlchemy that we want to be able to use
        # the same in-memory database object from different threads
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
async def client_fixture(session: Session):
    # Define the new function that will be the new dependency override.
    def get_session_override():
        # This function will return a different session than the one that
        # would be returned by the original get_session function.
        return session

    # here we are telling the FastAPI app to use get_session_override instead of get_session
    # in all the places in the code that depend on get_session
    app.dependency_overrides[get_session] = get_session_override
    # We create a TestClient for the FastAPI app and put it in the variable client.
    # client = TestClient(app)
    # yield client
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
    # After we are done with the dependency override, we can restore the application back to normal,
    # by removing all the values in this dictionary app.dependency_overrides
    app.dependency_overrides.clear()


@pytest.fixture(name="get_token")
async def get_token(client: AsyncClient):
    response = await client.post(
        "/token",
        data={"username": "abc", "password": "abc@123"},
        headers={"content-type": "application/x-www-form-urlencoded",},
    )
    response_data = response.json()
    return response_data["access_token"]


@pytest.mark.asyncio
async def test_login(client: AsyncClient):
    response = await client.post(
        "/token",
        data={"username": "abc", "password": "abc@123"},
        headers={"content-type": "application/x-www-form-urlencoded",},
    )
    response_data = response.json()
    print(response_data)
    assert response.status_code == 200
    assert "access_token" in response_data
    assert response_data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_create_hero(client: AsyncClient, get_token: str):
    # use this client to talk to the API and send a POST HTTP operation, creating a new hero.
    response = await client.post(
        "/heroes/",
        json={"name": "Deadpond", "secret_name": "Dive Wilson"},
        headers={"Authorization": f"Bearer {get_token}"},
    )
    data = response.json()
    print(data)
    # hero created response - 201
    assert response.status_code == 201
    assert data["name"] == "Deadpond"
    assert data["secret_name"] == "Dive Wilson"
    assert data["age"] is None
    assert data["id"] is not None


@pytest.mark.asyncio
async def test_create_hero_incomplete(client: AsyncClient, get_token: str):
    # No secret_name
    response = await client.post(
        "/heroes/",
        json={"name": "Deadpond"},
        headers={"Authorization": f"Bearer {get_token}"},
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_hero_invalid(client: AsyncClient, get_token: str):
    # secret_name has an invalid type
    response = await client.post(
        "/heroes/",
        json={
            "name": "Deadpond",
            "secret_name": {"message": "Do you wanna know my secret identity?"},
        },
        headers={"Authorization": f"Bearer {get_token}"},
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_read_heroes(session: Session, client: AsyncClient):
    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
    hero_2 = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48)
    session.add(hero_1)
    session.add(hero_2)
    session.commit()

    response = await client.get("/heroes/")
    data = response.json()

    assert response.status_code == 200

    assert len(data) == 2
    assert data[0]["name"] == hero_1.name
    assert data[0]["secret_name"] == hero_1.secret_name
    assert data[0]["age"] == hero_1.age
    assert data[0]["id"] == hero_1.id
    assert data[1]["name"] == hero_2.name
    assert data[1]["secret_name"] == hero_2.secret_name
    assert data[1]["age"] == hero_2.age
    assert data[1]["id"] == hero_2.id


@pytest.mark.asyncio
async def test_read_hero(session: Session, client: AsyncClient):
    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
    session.add(hero_1)
    session.commit()

    response = await client.get(f"/heroes/{hero_1.id}")
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == hero_1.name
    assert data["secret_name"] == hero_1.secret_name
    assert data["age"] == hero_1.age
    assert data["id"] == hero_1.id


@pytest.mark.asyncio
async def test_update_hero(session: Session, client: AsyncClient, get_token: str):
    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
    session.add(hero_1)
    session.commit()

    response = await client.patch(
        f"/heroes/{hero_1.id}",
        json={"name": "Deadpuddle"},
        headers={"Authorization": f"Bearer {get_token}"},
    )
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == "Deadpuddle"
    assert data["secret_name"] == "Dive Wilson"
    assert data["age"] is None
    assert data["id"] == hero_1.id


@pytest.mark.asyncio
async def test_delete_hero(session: Session, client: AsyncClient, get_token: str):
    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
    session.add(hero_1)
    session.commit()

    response = await client.delete(
        f"/heroes/{hero_1.id}", headers={"Authorization": f"Bearer {get_token}"},
    )
    hero_in_db = session.get(Hero, hero_1.id)

    assert response.status_code == 200
    assert hero_in_db is None
