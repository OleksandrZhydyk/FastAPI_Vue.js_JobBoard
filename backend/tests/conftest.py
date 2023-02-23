import asyncio
import os

import alembic
import pytest
import pytest_asyncio
from alembic.config import Config
from fastapi import FastAPI
from httpx import AsyncClient


os.environ['TESTING'] = 'True'

from db.base import async_session, engine, Base
from schemas.user import UserOut
from core.security import hash_password, create_access_token
from db.models.users import User


@pytest.fixture(autouse=True, scope="module")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(autouse=True, scope="module")
def app() -> FastAPI:
    from main import get_application  # local import for testing purpose

    app = get_application()
    return app


@pytest.fixture(autouse=True)
def db_models():
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.create_all)
    config = Config("alembic.ini")
    alembic.command.upgrade(config, "head")
    yield
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all)
    alembic.command.downgrade(config, "base")


@pytest_asyncio.fixture
async def session():
    session = async_session()
    yield session


@pytest_asyncio.fixture
async def create_user(session):
    db_obj = User(
        email="test@test.com",
        name="Test",
        is_active=True,
        hashed_password=hash_password("testpass")
    )
    session.add(db_obj)
    await session.commit()
    return db_obj


@pytest_asyncio.fixture
async def create_company(session):
    db_obj = User(
        email="company@test.com",
        name="Test",
        is_company=True,
        is_active=True,
        hashed_password=hash_password("testpass")
    )
    session.add(db_obj)
    await session.commit()
    return db_obj


@pytest_asyncio.fixture
async def create_superuser(session):
    db_obj = User(
        email="superuser@test.com",
        name="Test",
        is_active=True,
        is_superuser=True,
        hashed_password=hash_password("superuserpass")
    )
    session.add(db_obj)
    await session.commit()
    return db_obj


@pytest_asyncio.fixture
async def client(app: FastAPI) -> AsyncClient:
    async with AsyncClient(
        app=app,
        base_url="http://localhost",
        headers={"Content-Type": "application/json"}
    ) as client:
        yield client


@pytest_asyncio.fixture
def token(create_user: UserOut) -> str:
    access_token = create_access_token(data={"sub": create_user.email, "scopes": ["auth"]})
    return access_token


@pytest_asyncio.fixture
def company_token(create_company: UserOut) -> str:
    access_token = create_access_token(data={"sub": create_company.email, "scopes": ["auth", "company"]})
    return access_token


@pytest_asyncio.fixture
def superuser_token(create_superuser: UserOut) -> str:
    access_token = create_access_token(data={"sub": create_superuser.email, "scopes": ["auth", "superuser"]})
    return access_token


@pytest_asyncio.fixture
def authorized_client(client: AsyncClient, token: str) -> AsyncClient:
    client.headers = {
        "Authorization": f"Bearer {token}",
        **client.headers,
    }
    return client


@pytest_asyncio.fixture
def company_client(client: AsyncClient, company_token: str) -> AsyncClient:
    client.headers = {
        "Authorization": f"Bearer {company_token}",
        **client.headers,
    }
    return client


@pytest_asyncio.fixture
def superuser_client(client: AsyncClient, superuser_token: str) -> AsyncClient:
    client.headers = {
        "Authorization": f"Bearer {superuser_token}",
        **client.headers,
    }
    return client
