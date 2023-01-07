import asyncio
import os

import alembic
import pytest
import pytest_asyncio
from alembic.config import Config
from fastapi import FastAPI
from httpx import AsyncClient

os.environ['TESTING'] = 'True'


@pytest.fixture(scope="session")
def app() -> FastAPI:
    from src.main import get_application  # local import for testing purpose

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


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture()
async def async_client(app: FastAPI) -> AsyncClient:
    async with AsyncClient(
        app=app,
        base_url="http://localhost",
        headers={"Content-Type": "application/json"}
    ) as client:
        yield client
