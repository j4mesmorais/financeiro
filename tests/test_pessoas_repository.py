# tests/test_pessoas_repository.py

import pytest
from datetime import date

from src.infrastructure.db.repositories.pessoas import PessoaRepository
from src.core.pessoas.entity import Pessoa
from src.core.pessoas.model import PessoaModel

@pytest.mark.asyncio
async def test_create_and_get(async_session):
    repo = PessoaRepository(async_session)

    # create
    nova = Pessoa(nome="James", data_nascimento=date(2025, 6, 17), flag="C")
    criado: PessoaModel = await repo.create(nova)
    assert criado.id is not None
    assert criado.nome == "James"
    assert criado.data_nascimento == date(2025, 6, 17)
    assert criado.flag == "C"

    # get_by_id
    buscado = await repo.get_by_id(criado.id)
    assert buscado is not None
    assert buscado.nome == criado.nome
    assert buscado.flag == criado.flag

@pytest.mark.asyncio
async def test_list_update_delete(async_session):
    repo = PessoaRepository(async_session)

    # seed inicial
    p1 = await repo.create(Pessoa(nome="Ana Paula", flag="C"))
    p2 = await repo.create(Pessoa(nome="Carla Souza", flag="C"))

    # list
    todas = await repo.list()
    ids = {p.id for p in todas}
    assert p1.id in ids
    assert p2.id in ids

    # update
    atualizado = await repo.update(p1.id, Pessoa(id=p1.id, nome="Ana P.", flag="C"))
    assert atualizado.nome == "Ana P."

    # delete
    ok = await repo.delete(p2.id)
    assert ok
    none = await repo.get_by_id(p2.id)
    assert none is None
