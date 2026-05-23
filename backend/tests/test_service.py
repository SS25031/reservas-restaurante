"""Tests for ReservaService (post-refactor API)."""

from datetime import date

import pytest

from config import Configuracion
from exceptions import (
    CapacidadInsuficienteError,
    ConflictoHorarioError,
    LimiteDiarioExcedidoError,
    MesaNoDisponibleError,
    ReservaNoEncontradaError,
    ValorInvalidoError,
)
from models import Reserva, Turno
from tests.conftest import construir_mesas
from services import ReservaService

LUNES = date(2026, 6, 1)
MARTES = date(2026, 6, 2)


def make_args(**overrides):
    base = dict(
        cliente="Ana",
        telefono="7000-0000",
        personas=2,
        fecha=LUNES,
        turno=Turno.NOCHE,
    )
    base.update(overrides)
    return base


# ---------------- hacer_reserva ----------------

def test_hacer_reserva_exitosa(service: ReservaService):
    reserva = service.hacer_reserva(**make_args())
    assert isinstance(reserva, Reserva)
    assert reserva.id == 1
    assert reserva.numero_mesa == 1


def test_hacer_reserva_asigna_mesa_apropiada_para_el_grupo(service: ReservaService):
    reserva = service.hacer_reserva(**make_args(personas=6))
    assert reserva.numero_mesa == 11  # rango 11-15 -> cap 6


def test_grupo_excesivo_lanza_capacidad_insuficiente(service: ReservaService):
    with pytest.raises(CapacidadInsuficienteError):
        service.hacer_reserva(**make_args(personas=11))


def test_personas_cero_o_negativo_es_invalido(service: ReservaService):
    with pytest.raises(ValorInvalidoError):
        service.hacer_reserva(**make_args(personas=0))
    with pytest.raises(ValorInvalidoError):
        service.hacer_reserva(**make_args(personas=-3))


def test_cliente_vacio_es_invalido(service: ReservaService):
    with pytest.raises(ValorInvalidoError):
        service.hacer_reserva(**make_args(cliente="   "))


def test_limite_diario(service: ReservaService):
    for _ in range(25):
        service.hacer_reserva(**make_args(personas=2))
    with pytest.raises(LimiteDiarioExcedidoError):
        service.hacer_reserva(**make_args(personas=2))


def test_limite_diario_personalizable():
    svc = ReservaService(
        construir_mesas(), config=Configuracion(max_reservas_por_dia=2)
    )
    svc.hacer_reserva(**make_args(personas=2))
    svc.hacer_reserva(**make_args(personas=4))
    with pytest.raises(LimiteDiarioExcedidoError):
        svc.hacer_reserva(**make_args(personas=2))


def test_dos_reservas_mismo_turno_obtienen_mesas_distintas(service: ReservaService):
    r1 = service.hacer_reserva(**make_args(personas=2))
    r2 = service.hacer_reserva(**make_args(personas=2))
    assert r1.numero_mesa != r2.numero_mesa


def test_misma_mesa_disponible_en_turno_distinto(service: ReservaService):
    r1 = service.hacer_reserva(**make_args(turno=Turno.MANANA))
    r2 = service.hacer_reserva(**make_args(turno=Turno.NOCHE))
    assert r1.numero_mesa == r2.numero_mesa == 1


def test_grupo_pequeno_cae_a_mesa_mas_grande_si_las_pequenas_ocupadas(
    service: ReservaService,
):
    # Las 5 mesas de capacidad 2 quedan tomadas en el turno NOCHE.
    for _ in range(5):
        service.hacer_reserva(**make_args(personas=2, turno=Turno.NOCHE))
    # La siguiente reserva de 2 personas cae a mesa 6 (capacidad 4).
    siguiente = service.hacer_reserva(**make_args(personas=2, turno=Turno.NOCHE))
    assert siguiente.numero_mesa == 6


def test_si_todas_las_mesas_ocupadas_lanza_mesa_no_disponible(service: ReservaService):
    # Llenar todas las 25 mesas del turno NOCHE con grupos pequeños.
    for _ in range(25):
        service.hacer_reserva(**make_args(personas=2, turno=Turno.NOCHE))
    # Para el mismo turno, no hay mesa libre — pero el límite diario también
    # se alcanza primero, así que esperamos LimiteDiarioExcedido.
    with pytest.raises(LimiteDiarioExcedidoError):
        service.hacer_reserva(**make_args(personas=2, turno=Turno.NOCHE))


def test_mesa_no_disponible_cuando_limite_diario_alto():
    svc = ReservaService(
        construir_mesas(), config=Configuracion(max_reservas_por_dia=999)
    )
    # Llenar el turno MANANA con 25 reservas distintas
    for _ in range(25):
        svc.hacer_reserva(**make_args(personas=2, turno=Turno.MANANA))
    # Una 26ª de 2 personas: el límite diario no se aplica (999), pero
    # las 25 mesas están todas tomadas en el turno → MesaNoDisponibleError.
    with pytest.raises(MesaNoDisponibleError):
        svc.hacer_reserva(**make_args(personas=2, turno=Turno.MANANA))


# ---------------- cancelar_reserva ----------------

def test_cancelar_reserva_existente(service: ReservaService):
    reserva = service.hacer_reserva(**make_args())
    service.cancelar_reserva(reserva.id)
    assert service.total_reservas == 0


def test_cancelar_inexistente_lanza_no_encontrada(service: ReservaService):
    with pytest.raises(ReservaNoEncontradaError):
        service.cancelar_reserva(reserva_id=999)


def test_cancelar_libera_la_mesa(service: ReservaService):
    r1 = service.hacer_reserva(**make_args())
    service.cancelar_reserva(r1.id)
    libres = service.mesas_disponibles(fecha=LUNES, turno=Turno.NOCHE)
    assert any(m.numero == r1.numero_mesa for m in libres)


# ---------------- editar_reserva ----------------

def test_editar_a_horario_libre(service: ReservaService):
    reserva = service.hacer_reserva(**make_args())
    actualizada = service.editar_reserva(
        reserva.id, nueva_fecha=MARTES, nuevo_turno=Turno.TARDE
    )
    assert actualizada.fecha == MARTES
    assert actualizada.turno is Turno.TARDE


def test_editar_a_horario_con_conflicto_lanza(service: ReservaService):
    service.hacer_reserva(**make_args())  # mesa 1, LUNES, NOCHE
    r2 = service.hacer_reserva(**make_args(fecha=MARTES))  # mesa 1, MARTES, NOCHE
    with pytest.raises(ConflictoHorarioError):
        service.editar_reserva(r2.id, nueva_fecha=LUNES, nuevo_turno=Turno.NOCHE)


def test_editar_aplica_limite_diario_a_nueva_fecha(service: ReservaService):
    # Llenamos MARTES al máximo.
    for _ in range(25):
        service.hacer_reserva(**make_args(personas=2, fecha=MARTES))
    # Una reserva en LUNES.
    reserva_lunes = service.hacer_reserva(**make_args(personas=2, fecha=LUNES))
    # Moverla a MARTES debe rechazar.
    with pytest.raises(LimiteDiarioExcedidoError):
        service.editar_reserva(
            reserva_lunes.id, nueva_fecha=MARTES, nuevo_turno=Turno.MANANA
        )


def test_editar_inexistente_lanza_no_encontrada(service: ReservaService):
    with pytest.raises(ReservaNoEncontradaError):
        service.editar_reserva(999, nueva_fecha=LUNES, nuevo_turno=Turno.TARDE)


# ---------------- mesas_disponibles + buscar ----------------

def test_mesas_disponibles_excluye_reservadas(service: ReservaService):
    service.hacer_reserva(**make_args())
    libres = service.mesas_disponibles(fecha=LUNES, turno=Turno.NOCHE)
    assert len(libres) == 24


def test_todas_las_reservas_ordenadas_por_fecha(service: ReservaService):
    r_martes = service.hacer_reserva(**make_args(fecha=MARTES))
    r_lunes = service.hacer_reserva(**make_args(fecha=LUNES))
    listadas = service.todas_las_reservas()
    assert [r.id for r in listadas] == [r_lunes.id, r_martes.id]


def test_buscar_por_id_inexistente_lanza(service: ReservaService):
    with pytest.raises(ReservaNoEncontradaError):
        service.buscar_por_id(123)
