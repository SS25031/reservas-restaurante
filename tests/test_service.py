"""Characterization tests for the current ReservaService API.

Pins existing behavior (tuple returns, dia: int, no customer data) so we
can refactor with confidence. Rewritten in Task 8 once the API is changed.
"""

from reservas_restaurante.services import MAX_RESERVAS_POR_DIA, ReservaService


def test_hacer_reserva_exitosa(service: ReservaService):
    ok, mensaje, reserva = service.hacer_reserva(personas=2, dia=1, turno=1)
    assert ok is True
    assert "exito" in mensaje.lower()
    assert reserva is not None
    assert reserva.id == 1
    assert reserva.numero_mesa == 1


def test_grupo_excede_capacidad_maxima(service: ReservaService):
    ok, mensaje, reserva = service.hacer_reserva(personas=11, dia=1, turno=1)
    assert ok is False
    assert reserva is None
    assert "capacidad" in mensaje.lower()


def test_dos_reservas_mismo_turno_obtienen_mesas_distintas(service: ReservaService):
    _, _, r1 = service.hacer_reserva(personas=2, dia=1, turno=1)
    _, _, r2 = service.hacer_reserva(personas=2, dia=1, turno=1)
    assert r1.numero_mesa != r2.numero_mesa


def test_limite_diario_se_aplica(service: ReservaService):
    for _ in range(MAX_RESERVAS_POR_DIA):
        ok, *_ = service.hacer_reserva(personas=2, dia=1, turno=1)
        assert ok is True
    ok, mensaje, _ = service.hacer_reserva(personas=2, dia=1, turno=1)
    assert ok is False
    assert "limite" in mensaje.lower()


def test_cancelar_reserva_existente(service: ReservaService):
    _, _, reserva = service.hacer_reserva(personas=2, dia=1, turno=1)
    ok, _ = service.cancelar_reserva(reserva.id)
    assert ok is True
    assert service.total_reservas == 0


def test_cancelar_reserva_inexistente(service: ReservaService):
    ok, mensaje = service.cancelar_reserva(reserva_id=999)
    assert ok is False
    assert "no se encontro" in mensaje.lower()


def test_editar_reserva_a_horario_libre(service: ReservaService):
    _, _, reserva = service.hacer_reserva(personas=2, dia=1, turno=1)
    ok, _ = service.editar_reserva(reserva.id, nuevo_dia=2, nuevo_turno=2)
    assert ok is True
    actualizada = service.buscar_por_id(reserva.id)
    assert actualizada.dia == 2
    assert actualizada.turno == 2


def test_mesas_disponibles_excluye_reservadas(service: ReservaService):
    service.hacer_reserva(personas=2, dia=1, turno=1)
    libres = service.mesas_disponibles(dia=1, turno=1)
    assert all(m.numero != 1 for m in libres)
    assert len(libres) == 24
