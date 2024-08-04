import asyncio

import pytest
from httpx import ASGITransport, AsyncClient

from app.__main__ import app as fastapi_app
from app.config import settings
from app.database import Base, async_session, engine
from app.todo_list.models import Task  # noqa
from app.users.models import User  # noqa


@pytest.fixture(scope="function", autouse=True)
async def prepare_database():
    assert settings.MODE == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def ac():
    async with AsyncClient(transport=ASGITransport(app=fastapi_app), base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="function")
async def session():
    async with async_session() as session:
        yield session
