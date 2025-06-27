# tests/conftest.py

import os
import sys

# torna 'src/' importável
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

import pytest
import pytest_asyncio
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from src.core.pessoas.model import Base

@pytest.fixture(scope="session")
def test_database_url():
    return (
        os.getenv("TEST_DATABASE_URL")
        or os.getenv("DATABASE_URL")
        or "postgresql://postgres:postgres@localhost:5432/financeiro"
    )

@pytest.fixture(scope="session")
def sync_engine(test_database_url):
    # para o teste de migrações, sem alterar pool
    engine = create_engine(test_database_url, poolclass=NullPool, echo=False)
    Base.metadata.create_all(engine)
    return engine

@pytest_asyncio.fixture(scope="session")
async def async_engine(test_database_url):
    # ajusta URL para asyncpg
    url = (
        test_database_url
        if test_database_url.startswith("postgresql+asyncpg://")
        else test_database_url.replace("postgresql://", "postgresql+asyncpg://", 1)
    )
    # NÃO especificar poolclass aqui: usar o padrão
    engine = create_async_engine(url, echo=False)
    yield engine
    await engine.dispose()

@pytest_asyncio.fixture
async def async_session(async_engine):
    # antes de tudo, garanta o schema
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # sessão para os testes
    Factory = sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)
    async with Factory() as session:
        yield session
