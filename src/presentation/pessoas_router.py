# src/presentation/pessoas_router.py

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.presentation.schemas.pessoas import PessoaCreate, PessoaRead, PessoaUpdate
from src.application.pessoas_service import PessoaService
from src.infrastructure.db.session import get_session
from src.infrastructure.auth.jwt_utils import get_current_user

router = APIRouter(
    prefix="/pessoas",
    tags=["Pessoas"],
)

@router.post("/", response_model=PessoaRead, status_code=status.HTTP_201_CREATED)
async def create_pessoa(
    payload: PessoaCreate,
    session: AsyncSession = Depends(get_session),
    current_user: str = Depends(get_current_user),
) -> PessoaRead:
    service = PessoaService(session)
    try:
        pessoa = await service.create_pessoa(
            nome=payload.nome,
            celular=payload.celular,
            cpf=payload.cpf,
            data_nascimento=payload.data_nascimento,
            flag=payload.flag,
        )
        return pessoa
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/{pessoa_id}", response_model=PessoaRead)
async def get_pessoa(
    pessoa_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: str = Depends(get_current_user),
) -> PessoaRead:
    service = PessoaService(session)
    try:
        return await service.get_pessoa(pessoa_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.get("/", response_model=List[PessoaRead])
async def list_pessoas(
    skip: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_session),
    current_user: str = Depends(get_current_user),
) -> List[PessoaRead]:
    service = PessoaService(session)
    return await service.list_pessoas(skip=skip, limit=limit)

@router.put("/{pessoa_id}", response_model=PessoaRead)
async def update_pessoa(
    pessoa_id: int,
    payload: PessoaUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: str = Depends(get_current_user),
) -> PessoaRead:
    service = PessoaService(session)
    try:
        return await service.update_pessoa(
            pessoa_id=pessoa_id,
            nome=payload.nome,
            celular=payload.celular,
            cpf=payload.cpf,
            data_nascimento=payload.data_nascimento,
            flag=payload.flag,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.delete("/{pessoa_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_pessoa(
    pessoa_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: str = Depends(get_current_user),
) -> None:
    service = PessoaService(session)
    try:
        await service.delete_pessoa(pessoa_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
