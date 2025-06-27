#!/usr/bin/env python3
"""
Valida que a tabela 'pessoas' existe no seu Postgres de desenvolvimento.
"""

import os
import sys
from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect

# 1) Ajusta sys.path para encontrar o pacote src/
sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)

# 2) Carrega .env da raiz
dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))
load_dotenv(dotenv_path)

# 3) Importa Base do seu modelo
from core.pessoas.model import Base

def main():
    url = os.getenv("DATABASE_URL")
    if not url:
        print("❌ DATABASE_URL não definido no .env")
        sys.exit(1)

    engine = create_engine(url, echo=False)
    # cria (ou atualiza) todas as tabelas
    Base.metadata.create_all(engine)

    inspector = inspect(engine)
    tables = inspector.get_table_names()

    if "pessoas" in tables:
        print("✅ Tabela 'pessoas' encontrada!")
        sys.exit(0)
    else:
        print("❌ Tabela 'pessoas' NÃO encontrada. Tabelas disponíveis:", tables)
        sys.exit(2)

if __name__ == "__main__":
    main()
