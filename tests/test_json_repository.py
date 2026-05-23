"""Tests for JsonReservaRepository roundtrip serialization."""

from datetime import date
from pathlib import Path

from models import Reserva, Turno
from repositories.json_repo import JsonReservaRepository


def _sample_reservas() -> list[Reserva]:
    return [
        Reserva(
            id=1,
            fecha=date(2026, 6, 1),
            turno=Turno.NOCHE,
            numero_mesa=3,
            cliente="Ana Pérez",
            telefono="7000-1234",
            personas=2,
        ),
        Reserva(
            id=2,
            fecha=date(2026, 6, 2),
            turno=Turno.MANANA,
            numero_mesa=11,
            cliente="Luis Méndez",
            telefono="7000-9999",
            personas=6,
        ),
    ]


def test_guardar_y_cargar_roundtrip(tmp_path: Path):
    archivo = tmp_path / "reservas.json"
    repo = JsonReservaRepository(archivo)
    repo.guardar(_sample_reservas(), ultimo_id=2)

    cargadas, ultimo_id = repo.cargar()
    assert ultimo_id == 2
    assert len(cargadas) == 2
    assert cargadas[0].cliente == "Ana Pérez"
    assert cargadas[0].fecha == date(2026, 6, 1)
    assert cargadas[0].turno is Turno.NOCHE
    assert cargadas[1].turno is Turno.MANANA


def test_cargar_archivo_inexistente_devuelve_vacio(tmp_path: Path):
    archivo = tmp_path / "no-existe.json"
    repo = JsonReservaRepository(archivo)
    reservas, ultimo_id = repo.cargar()
    assert reservas == []
    assert ultimo_id == 0


def test_guardar_lista_vacia_se_recupera_vacia(tmp_path: Path):
    archivo = tmp_path / "vacio.json"
    repo = JsonReservaRepository(archivo)
    repo.guardar([], ultimo_id=0)
    reservas, ultimo_id = repo.cargar()
    assert reservas == []
    assert ultimo_id == 0


def test_guardar_crea_directorios_padres(tmp_path: Path):
    archivo = tmp_path / "sub" / "dir" / "reservas.json"
    repo = JsonReservaRepository(archivo)
    repo.guardar([], ultimo_id=0)
    assert archivo.exists()
