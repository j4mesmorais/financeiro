# src/infrastructure/auth/jwt_utils.py

import os
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from dotenv import load_dotenv

# 1) Carrega .env
load_dotenv()

# 2) Segredo e configurações HS256
JWT_SECRET = os.getenv("JWT_SECRET")
if not JWT_SECRET:
    raise RuntimeError("JWT_SECRET não definido no .env")
ALGORITHM = "HS256"

# Esquema Bearer simples
security = HTTPBearer()

def decode_access_token(token: str) -> Dict[str, Any]:
    """
    Decodifica o JWT e retorna um dict com campos essenciais.
    Espera encontrar no payload:
      - id: int
      - email: str
      - isSuperUser: bool
    """
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token expirado")
    except jwt.PyJWTError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token inválido")

    user_id = payload.get("id")
    email = payload.get("email")
    is_superuser = payload.get("isSuperUser")

    if user_id is None or email is None or is_superuser is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token inválido")

    return {
        "id": user_id,
        "email": email,
        "is_superuser": is_superuser
    }

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict[str, Any]:
    """
    Extrai o usuário atual a partir do header Authorization: Bearer <token>.
    Retorna um dict com id, email e is_superuser.
    """
    token = credentials.credentials
    return decode_access_token(token)
