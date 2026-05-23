"""Pruebas del SqlAlchemyMesaRepository."""

from reservas_app.models import Mesa
from reservas_app.repositories.mesa_repo import SqlAlchemyMesaRepository


def test_listar_vacio(db_session):
    repo = SqlAlchemyMesaRepository(db_session)
    assert repo.listar() == []


def test_reemplazar_y_listar(db_session):
    repo = SqlAlchemyMesaRepository(db_session)
    mesas = [
        Mesa(numero=1, capacidad=2, pos_x=10.0, pos_y=20.0),
        Mesa(numero=2, capacidad=4),
    ]
    repo.reemplazar_todas(mesas)

    cargadas = repo.listar()
    assert len(cargadas) == 2
    assert cargadas[0].numero == 1
    assert cargadas[0].pos_x == 10.0
    assert cargadas[1].capacidad == 4


def test_reemplazar_sobrescribe_layout_previo(db_session):
    repo = SqlAlchemyMesaRepository(db_session)
    repo.reemplazar_todas([Mesa(numero=1, capacidad=2)])
    repo.reemplazar_todas([Mesa(numero=5, capacidad=8)])

    cargadas = repo.listar()
    assert len(cargadas) == 1
    assert cargadas[0].numero == 5
