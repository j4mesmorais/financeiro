# src/core/pessoas/entity.py

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional

@dataclass
class Pessoa:
    nome: str  # único campo obrigatório
    id: Optional[int] = field(default=None)
    celular: Optional[str] = None
    cpf: Optional[str] = None
    data_nascimento: Optional[date] = None
    flag: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)

    def __post_init__(self):
        if not self.nome or not self.nome.strip():
            raise ValueError("O nome da pessoa não pode ser vazio.")
