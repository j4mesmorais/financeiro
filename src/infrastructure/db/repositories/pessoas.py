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
        # Build update values dict, excluding None values
        update_values = {}
        for attr in ("nome", "celular", "cpf", "data_nascimento", "flag"):
            val = getattr(pessoa, attr)
            if val is not None:
                update_values[attr] = val
        
        if not update_values:
            # No values to update, return existing record
            return await self.get_by_id(pessoa_id)
        
        # Perform direct update query
        from sqlalchemy import update
        stmt = update(PessoaModel).where(PessoaModel.id == pessoa_id).values(**update_values)
        result = await self.session.execute(stmt)
        
        if result.rowcount == 0:
            # No rows affected, record doesn't exist
            return None
            
        await self.session.commit()
        # Return updated record
        return await self.get_by_id(pessoa_id)

    async def delete(self, pessoa_id: int) -> bool:
        # Perform direct delete query
        from sqlalchemy import delete
        stmt = delete(PessoaModel).where(PessoaModel.id == pessoa_id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        
        # Return True if a row was actually deleted
        return result.rowcount > 0
