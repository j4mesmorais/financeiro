# src/core/pessoas/model.py

from datetime import datetime
from sqlalchemy import Column, Integer, String, Date, Boolean, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class PessoaModel(Base):
    __tablename__ = "pessoas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    celular = Column(String(20), nullable=True)
    cpf = Column(String(14), nullable=True)
    data_nascimento = Column(Date, nullable=True)
    flag = Column(String(1), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
