# Financeiro API

Uma API RESTful para gestão financeira de pessoas, lançamentos e centros de responsabilidade, construída em Python com FastAPI e seguindo a arquitetura hexagonal.

## Visão Geral

Este serviço expõe endpoints para CRUD de **Pessoas**, protegido por JWT HS256 — ideal para ser consumido por front-ends ou outros microsserviços.

### Funcionalidades

- Registro, leitura, listagem, atualização e remoção de registros de pessoas
- Autenticação via token JWT (Bearer) compartilhado com serviço de login externo
- Documentação automática Swagger/OpenAPI (via FastAPI + fastapi-mcp)
- Health check em `/health`

## Arquitetura

Organizado em camadas hexagonais:

```
financeiro/
├── src/                # Código-fonte da aplicação
│   ├── core/           # Entidades e validações de domínio
│   ├── application/    # Serviços / casos de uso
│   ├── infrastructure/ # Adaptadores externos (DB, JWT)
│   └── presentation/   # FastAPI routers & schemas
├── tests/              # Testes de migrações e CRUD
├── scripts/            # Scripts standalone para validações diretas
├── .env                # Variáveis de ambiente sensíveis
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## Stack Tecnológica

- **Python 3.11+**
- **FastAPI** para framework web
- **fastapi-mcp** para modularização e docs
- **SQLAlchemy (Async)** + **Alembic** para ORM e migrações
- **PostgreSQL** como banco de dados
- **JWT HS256** (pyjwt) para autenticação
- **pytest / pytest-asyncio** para testes automatizados

## Começando

1. **Clone** o repositório:
   ```bash
   git clone <URL-DO-REPO> && cd financeiro
   ```
2. **Configure** as variáveis em `.env` (crie a partir de `.env.example`):
   ```ini
   DATABASE_URL=postgresql://user:pass@host:5432/financeiro
   JWT_SECRET=<chave_secreta_compartilhada>
   ```
3. **Instale** as dependências:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
4. **Crie** o schema do banco (Alembic):
   ```bash
   alembic upgrade head
   ```
5. **Execute** localmente:
   ```bash
   uvicorn src.main:app --reload
   ```
6. **Acesse** no navegador:
   - Swagger UI: http://localhost:8000/docs
   - Health check:  http://localhost:8000/health

## Testes

- **Pytest** para cobertura de migrações e CRUD:
  ```bash
  export PYTHONPATH="$PWD"
  pytest
  ```
- **Scripts standalone** em `scripts/`:
  ```bash
  ./scripts/test_migrations.py
  ./scripts/test_pessoas_crud.py
  ```

## Containerização

- **Dockerfile** na raiz
- **docker-compose.yml** orquestra `app` + `postgres`

Para subir tudo:
```bash
docker-compose up --build
```

## Contribuindo

1. Abra uma issue para discutir a feature.
2. Crie uma branch (`git checkout -b feat/minha-feature`).
3. Faça commit (`git commit -m 'Adiciona XYZ'`).
4. Envie um pull request.

---

Desenvolvido com base em boas práticas de arquitetura hexagonal e clean code. Boa codificação!

