#!/usr/bin/env python3
"""
Executa um ciclo completo de CRUD em PessoaRepository contra
seu Postgres de desenvolvimento.
"""

import os
import sys
import asyncio
from datetime import date
from dotenv import load_dotenv

# 1) Ajusta sys.path para encontrar o pacote src/
sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)

# 2) Carrega .env da raiz
dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))
load_dotenv(dotenv_path)

# 3) Imports
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from infrastructure.db.repositories.pessoas import PessoaRepository
from core.pessoas.entity import Pessoa

async def main():
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("❌ DATABASE_URL não definido no .env")
        sys.exit(1)

    # adapta para asyncpg
    if db_url.startswith("postgresql://"):
        db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)

    engine = create_async_engine(db_url, echo=False)
    AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

    async with AsyncSessionLocal() as session:
        repo = PessoaRepository(session)

        # CREATE
        print("➕ Criando Pessoa...")
        nova = Pessoa(nome="Script Teste", data_nascimento=date(2000,1,1), flag="C")
        #nova = Pessoa(nome="Script Teste")
        criado = await repo.create(nova)
        print(f"    ✔️  id={criado.id}, nome={criado.nome}")

        # READ
        buscado = await repo.get_by_id(criado.id)
        print(f"🔍 Lido: id={buscado.id}, nome={buscado.nome}")

        # LIST
        todos = await repo.list()
        print(f"📋 Total de pessoas: {len(todos)}")

        # UPDATE
        print("✏️  Atualizando nome...")
        atualizado = await repo.update(criado.id, Pessoa(id=criado.id, nome="Script Atualizado", flag="C"))
        print(f"    ✔️  Novo nome: {atualizado.nome}")

        # DELETE
        print("🗑️  Deletando registro...")
        deleted = await repo.delete(criado.id)
        print(f"    ✔️  Deletado: {deleted}")

    await engine.dispose()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print("❌ Erro durante CRUD:", e)
        sys.exit(1)
