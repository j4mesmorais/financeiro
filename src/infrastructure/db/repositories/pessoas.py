# src/infrastructure/db/repositories/pessoas.py

from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.pessoas.entity import Pessoa
from src.core.pessoas.model import PessoaModel

class PessoaRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, pessoa: Pessoa) -> PessoaModel:
        db_pessoa = PessoaModel(
            nome=pessoa.nome,
            celular=pessoa.celular,
            cpf=pessoa.cpf,
            data_nascimento=pessoa.data_nascimento,
            flag=pessoa.flag
        )
        self.session.add(db_pessoa)
        await self.session.commit()
        await self.session.refresh(db_pessoa)
        return db_pessoa

    async def get_by_id(self, pessoa_id: int) -> Optional[PessoaModel]:
        result = await self.session.execute(
            select(PessoaModel).where(PessoaModel.id == pessoa_id)
        )
        return result.scalars().first()

    async def list(self, skip: int = 0, limit: int = 100) -> List[PessoaModel]:
        result = await self.session.execute(
            select(PessoaModel).offset(skip).limit(limit)
        )
        return result.scalars().all()

    async def update(self, pessoa_id: int, pessoa: Pessoa) -> Optional[PessoaModel]:
        db_pessoa = await self.get_by_id(pessoa_id)
        if not db_pessoa:
            return None
        # Atualiza apenas campos não None
        for attr in ("nome", "celular", "cpf", "data_nascimento", "flag"):
            val = getattr(pessoa, attr)
            if val is not None:
                setattr(db_pessoa, attr, val)
        self.session.add(db_pessoa)
        await self.session.commit()
        await self.session.refresh(db_pessoa)
        return db_pessoa

    async def delete(self, pessoa_id: int) -> bool:
        db_pessoa = await self.get_by_id(pessoa_id)
        if not db_pessoa:
            return False
        await self.session.delete(db_pessoa)
        await self.session.commit()
        return True
