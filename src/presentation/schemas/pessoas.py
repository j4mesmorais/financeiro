from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, Field


class PessoaBase(BaseModel):
    nome: str = Field(..., description="Nome da pessoa", min_length=1)
    celular: Optional[str] = Field(None, description="Número de celular")
    cpf: Optional[str] = Field(None, description="CPF")
    data_nascimento: Optional[date] = Field(None, description="Data de nascimento")
    flag: Optional[str] = Field(None, description="Flag")


class PessoaCreate(PessoaBase):
    """Schema para criação de Pessoa."""
    pass


class PessoaUpdate(BaseModel):
    """Schema para atualização parcial de Pessoa."""
    nome: Optional[str] = Field(None, description="Nome da pessoa", min_length=1)
    celular: Optional[str] = Field(None, description="Número de celular")
    cpf: Optional[str] = Field(None, description="CPF")
    data_nascimento: Optional[date] = Field(None, description="Data de nascimento")
    flag: Optional[str] = Field(None, description="Flag")


class PessoaRead(PessoaBase):
    """Schema para leitura de Pessoa."""
    id: int = Field(..., description="ID da pessoa")
    created_at: datetime = Field(..., description="Timestamp de criação")

    class Config:
        orm_mode = True
