"""Pruebas del SqlAlchemyReservaRepository."""

from datetime import date

import pytest

from reservas_app.models import Reserva, Turno
from reservas_app.models.reserva import EstadoReserva
from reservas_app.repositories import SqlAlchemyMesaRepository, SqlAlchemyReservaRepository
from reservas_app.services import ReservaService
from tests._fixtures.mesas import construir_mesas


@pytest.fixture
def mesas_en_db(db_session):
    mesas = construir_mesas()
    SqlAlchemyMesaRepository(db_session).reemplazar_todas(mesas)
    return mesas


@pytest.fixture
def reserva_repo(db_session):
    return SqlAlchemyReservaRepository(db_session)


def test_cargar_sin_datos_devuelve_vacio(reserva_repo):
    reservas, ultimo_id = reserva_repo.cargar()
    assert reservas == []
    assert ultimo_id == 0


def test_guardar_y_cargar_roundtrip(reserva_repo, mesas_en_db):
    del mesas_en_db
    reservas = [
        Reserva(
            id=1,
            fecha=date(2026, 6, 1),
            turno=Turno.NOCHE,
            numero_mesa=1,
            cliente="Ana",
            telefono="7000-0000",
            email="ana@example.com",
            personas=2,
        ),
        Reserva(
            id=2,
            fecha=date(2026, 6, 2),
            turno=Turno.TARDE,
            numero_mesa=6,
            cliente="Luis",
            telefono="7000-0001",
            email="luis@example.com",
            personas=4,
        ),
    ]
    reserva_repo.guardar(reservas, ultimo_id=2)

    cargadas, ultimo_id = reserva_repo.cargar()
    assert ultimo_id == 2
    assert len(cargadas) == 2
    assert cargadas[0].email == "ana@example.com"
    assert cargadas[1].numero_mesa == 6


def test_guardar_reemplaza_snapshot_anterior(reserva_repo, mesas_en_db):
    del mesas_en_db
    primera = [
        Reserva(
            id=1,
            fecha=date(2026, 6, 1),
            turno=Turno.NOCHE,
            numero_mesa=1,
            cliente="Ana",
            telefono="7000-0000",
            email="ana@example.com",
            personas=2,
        )
    ]
    reserva_repo.guardar(primera, ultimo_id=1)

    segunda = [
        Reserva(
            id=2,
            fecha=date(2026, 6, 3),
            turno=Turno.MANANA,
            numero_mesa=2,
            cliente="Bea",
            telefono="7000-0002",
            email="bea@example.com",
            personas=2,
        )
    ]
    reserva_repo.guardar(segunda, ultimo_id=2)

    cargadas, ultimo_id = reserva_repo.cargar()
    assert len(cargadas) == 1
    assert cargadas[0].cliente == "Bea"
    assert ultimo_id == 2


def test_cargar_ignora_reservas_canceladas(reserva_repo, mesas_en_db):
    del mesas_en_db
    reservas = [
        Reserva(
            id=1,
            fecha=date(2026, 6, 1),
            turno=Turno.NOCHE,
            numero_mesa=1,
            cliente="Ana",
            telefono="7000-0000",
            email="ana@example.com",
            personas=2,
        ),
        Reserva(
            id=2,
            fecha=date(2026, 6, 2),
            turno=Turno.TARDE,
            numero_mesa=6,
            cliente="Luis",
            telefono="7000-0001",
            email="luis@example.com",
            personas=4,
            estado=EstadoReserva.CANCELADA,
        ),
    ]
    reserva_repo.guardar(reservas, ultimo_id=2)

    cargadas, ultimo_id = reserva_repo.cargar()
    assert len(cargadas) == 1
    assert cargadas[0].id == 1
    assert ultimo_id == 2


def test_servicio_roundtrip_via_repositorio(db_session, mesas_en_db):
    del mesas_en_db
    mesas = construir_mesas()
    repo = SqlAlchemyReservaRepository(db_session)
    service = ReservaService(mesas)
    service.hacer_reserva(
        cliente="Ana",
        telefono="7000-0000",
        email="ana@example.com",
        personas=2,
        fecha=date(2026, 6, 1),
        turno=Turno.NOCHE,
    )
    service.persistir_en(repo)

    recargado = ReservaService.cargar_desde(mesas, repo)
    assert recargado.total_reservas == 1
    assert recargado.todas_las_reservas()[0].email == "ana@example.com"
