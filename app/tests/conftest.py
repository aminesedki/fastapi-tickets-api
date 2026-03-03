from collections.abc import AsyncGenerator
from typing import Any

import pytest_asyncio
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from api.base import api_router  # adjust if needed
from db.base import Base
from db.deps import get_db  # IMPORTANT: same import used by your routes


def start_application() -> FastAPI:
    app = FastAPI()
    app.include_router(api_router)
    return app


@pytest_asyncio.fixture(scope="function")
async def engine(tmp_path) -> AsyncGenerator[Any, Any]:
    # unique sqlite file per test
    db_file = tmp_path / "test.db"
    database_url = f"sqlite+aiosqlite:///{db_file}"

    eng = create_async_engine(database_url, echo=False)

    # create schema
    async with eng.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield eng

    # drop schema and dispose
    async with eng.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await eng.dispose()


@pytest_asyncio.fixture(scope="function")
async def db_session(engine) -> AsyncGenerator[AsyncSession, Any]:
    SessionTesting = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
        autocommit=False,
    )

    async with SessionTesting() as session:
        yield session


# Alias fixture for your service tests that use "db"
@pytest_asyncio.fixture(scope="function")
async def db(db_session: AsyncSession) -> AsyncGenerator[AsyncSession, Any]:
    yield db_session


@pytest_asyncio.fixture(scope="function")
async def app() -> AsyncGenerator[FastAPI, Any]:
    _app = start_application()
    yield _app


@pytest_asyncio.fixture(scope="function")
async def client(app: FastAPI, db_session: AsyncSession) -> AsyncGenerator[AsyncClient, Any]:
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()
