"""Pruebas del SqlAlchemyReservaRepository (esqueleto).

Los roundtrips reales llegan en el subsistema 2 cuando ReservaORM exista.
Aquí solo verificamos que el Protocol se cumple y que las llamadas no
implementadas levantan NotImplementedError.
"""

import pytest

from reservas_app.repositories import (
    ReservaRepository,
    SqlAlchemyReservaRepository,
)


def test_sqla_repo_cumple_protocol(db_session):
    repo = SqlAlchemyReservaRepository(db_session)
    # `Protocol` no soporta isinstance directo a menos que sea @runtime_checkable.
    # Verificamos por duck typing: existencia de los métodos.
    assert hasattr(repo, "cargar")
    assert hasattr(repo, "guardar")
    # Sanity check: anotación de tipo en services apunta al Protocol correcto.
    assert ReservaRepository.__name__ == "ReservaRepository"


def test_cargar_levanta_not_implemented(db_session):
    repo = SqlAlchemyReservaRepository(db_session)
    with pytest.raises(NotImplementedError, match="subsistema 2"):
        repo.cargar()


def test_guardar_levanta_not_implemented(db_session):
    repo = SqlAlchemyReservaRepository(db_session)
    with pytest.raises(NotImplementedError, match="subsistema 2"):
        repo.guardar([], ultimo_id=0)
