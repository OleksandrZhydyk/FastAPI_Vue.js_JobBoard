import asyncio
import os

from fastapi_jwt_auth import AuthJWT
from sqlalchemy.dialects.postgresql import insert

os.environ["TESTING"] = "True"

import alembic
import pytest
import pytest_asyncio
from alembic.config import Config
from fastapi import FastAPI
from httpx import AsyncClient

from db.models.jobs import Job
from db.base import async_session
from schemas.user import UserOut
from core.security import hash_password
from db.models.users import User, association_table


@pytest.fixture(autouse=True, scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(autouse=True, scope="module")
def app() -> FastAPI:
    from main import get_application  # local import for testing purpose

    app = get_application()
    return app


@pytest_asyncio.fixture(autouse=True)
def db_models():
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.create_all)
    config = Config("alembic.ini")
    alembic.command.upgrade(config, "head")
    yield
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all)
    alembic.command.downgrade(config, "base")


@pytest.fixture
async def session():
    session = async_session()
    yield session


@pytest.fixture
async def create_user(session):
    db_obj = User(
        email="test@test.com",
        name="Test",
        is_active=True,
        hashed_password=hash_password("testpass"),
    )
    session.add(db_obj)
    await session.commit()
    return db_obj


@pytest.fixture
async def create_company(session):
    db_obj = User(
        email="company@test.com",
        name="Test",
        is_company=True,
        is_active=True,
        hashed_password=hash_password("testpass"),
    )
    session.add(db_obj)
    await session.commit()
    return db_obj


@pytest.fixture
async def create_job(session, create_company):
    db_obj = Job(
        email="test_job@test.com",
        title="TestJob",
        description="testpass",
        salary_from=10,
        salary_to=20,
        user_id=create_company.id,
    )
    session.add(db_obj)
    await session.commit()
    return db_obj


@pytest.fixture
async def apply_to_job(session, create_user, create_job):
    query = insert(association_table).values(
        {"user_id": create_user.id, "job_id": create_job.id}
    )
    await session.execute(query)
    try:
        await session.commit()
    except Exception:
        await session.rollback()


@pytest.fixture
async def create_superuser(session):
    db_obj = User(
        email="superuser@test.com",
        name="Test",
        is_active=True,
        is_superuser=True,
        hashed_password=hash_password("superuserpass"),
    )
    session.add(db_obj)
    await session.commit()
    return db_obj


@pytest.fixture
async def client(app: FastAPI) -> AsyncClient:
    async with AsyncClient(
        app=app,
        base_url="http://localhost",
        headers={"Content-Type": "application/json"},
    ) as client:
        yield client


@pytest.fixture
def authorize_obj():
    return AuthJWT()


@pytest.fixture
def token(create_user: UserOut, authorize_obj: AuthJWT) -> str:
    access_token = authorize_obj.create_access_token(subject=create_user.email)
    # access_token = create_access_token(
    #     data={"sub": create_user.email}
    # )
    return access_token


@pytest.fixture
def company_token(create_company: UserOut, authorize_obj: AuthJWT) -> str:
    access_token = authorize_obj.create_access_token(subject=create_company.email)
    return access_token


@pytest.fixture
def superuser_token(create_superuser: UserOut, authorize_obj: AuthJWT) -> str:
    access_token = authorize_obj.create_access_token(subject=create_superuser.email)
    return access_token


@pytest.fixture
def authorized_client(client: AsyncClient, token: str) -> AsyncClient:
    client.cookies = {
        "access_token_cookie": token,
        **client.cookies,
    }
    return client


@pytest.fixture
def company_client(client: AsyncClient, company_token: str) -> AsyncClient:
    client.cookies = {
        "access_token_cookie": company_token,
        **client.cookies,
    }
    return client


@pytest.fixture
def superuser_client(client: AsyncClient, superuser_token: str) -> AsyncClient:
    client.cookies = {
        "access_token_cookie": superuser_token,
        **client.cookies,
    }
    return client
