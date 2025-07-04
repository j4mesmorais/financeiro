from fastapi import FastAPI, Depends
from fastapi_mcp import FastApiMCP

from src.presentation.pessoas_router import router as pessoas_router
from src.infrastructure.db.session import get_session
from src.infrastructure.auth.jwt_utils import get_current_user

app = FastAPI(
    title="API Financeiro",
    version="0.1.0",
    docs_url="/docs",
    openapi_url="/openapi.json",
)

# Inclui o router de Pessoas (dependencies handled at endpoint level)
app.include_router(
    pessoas_router,
    #prefix="/pessoas",
    tags=["Pessoas"],
)

# Registra o MCP server em /mcp
mcp = FastApiMCP(app)
mcp.mount()

# Health check sem autenticação
@app.get("/health", tags=["Health"])
async def health():
    return {"status": "ok"}

# (Opcional) custom OpenAPI
# from fastapi.openapi.utils import get_openapi
# def custom_openapi(): ...
# app.openapi = custom_openapi
