# src/application/pessoas_service.py

from typing import List, Optional
from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.pessoas.entity import Pessoa
from src.core.pessoas.model import PessoaModel
from src.infrastructure.db.repositories.pessoas import PessoaRepository

class PessoaService:
    def __init__(self, session: AsyncSession):
        self.repo = PessoaRepository(session)

    async def create_pessoa(
        self,
        nome: str,
        celular: Optional[str] = None,
        cpf: Optional[str] = None,
        data_nascimento: Optional[date] = None,
        flag: Optional[str] = None,
    ) -> PessoaModel:
        # validação de domínio via entidade
        pessoa = Pessoa(
            nome=nome,
            celular=celular,
            cpf=cpf,
            data_nascimento=data_nascimento,
            flag=flag,
        )
        return await self.repo.create(pessoa)

    async def get_pessoa(self, pessoa_id: int) -> PessoaModel:
        db_pessoa = await self.repo.get_by_id(pessoa_id)
        if not db_pessoa:
            raise ValueError(f"Pessoa com id {pessoa_id} não encontrada.")
        return db_pessoa

    async def list_pessoas(self, skip: int = 0, limit: int = 100) -> List[PessoaModel]:
        return await self.repo.list(skip=skip, limit=limit)

    async def update_pessoa(
        self,
        pessoa_id: int,
        nome: Optional[str] = None,
        celular: Optional[str] = None,
        cpf: Optional[str] = None,
        data_nascimento: Optional[date] = None,
        flag: Optional[str] = None,
    ) -> PessoaModel:
        # usa entidade para validação parcial (nome não vazio se fornecido)
        if nome is not None and not nome.strip():
            raise ValueError("O nome da pessoa não pode ser vazio.")
        pessoa = Pessoa(
            id=pessoa_id,
            nome=nome or "",
            celular=celular,
            cpf=cpf,
            data_nascimento=data_nascimento,
            flag=flag,
        )
        updated = await self.repo.update(pessoa_id, pessoa)
        if not updated:
            raise ValueError(f"Pessoa com id {pessoa_id} não encontrada.")
        return updated

    async def delete_pessoa(self, pessoa_id: int) -> None:
        deleted = await self.repo.delete(pessoa_id)
        if not deleted:
            raise ValueError(f"Pessoa com id {pessoa_id} não encontrada.")
