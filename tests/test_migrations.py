# tests/test_migrations.py

from sqlalchemy import inspect
from src.core.pessoas.model import Base

def test_tables_created(sync_engine):
    """
    Garante que a tabela 'pessoas' existe no Postgres.
    """
    Base.metadata.create_all(sync_engine)
    inspector = inspect(sync_engine)
    tables = inspector.get_table_names()
    assert "pessoas" in tables, f"Tabelas encontradas: {tables}"
