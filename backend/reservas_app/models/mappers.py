"""Mapeo entre DTOs de dominio y modelos ORM."""

from datetime import date

from reservas_app.models import Mesa, Reserva, Turno
from reservas_app.models.orm import (
    CalendarDayORM,
    MesaORM,
    ReservaORM,
    TurnoConfigORM,
)
from reservas_app.models.reserva import EstadoReserva


def turno_a_str(turno: Turno) -> str:
    return turno.name


def turno_desde_str(valor: str) -> Turno:
    return Turno[valor]


def mesa_orm_a_dto(orm: MesaORM) -> Mesa:
    return Mesa(
        numero=orm.numero,
        capacidad=orm.capacidad,
        pos_x=orm.pos_x,
        pos_y=orm.pos_y,
    )


def mesa_dto_a_orm(dto: Mesa, restaurant_id: int) -> MesaORM:
    return MesaORM(
        restaurant_id=restaurant_id,
        numero=dto.numero,
        capacidad=dto.capacidad,
        pos_x=dto.pos_x,
        pos_y=dto.pos_y,
    )


def reserva_orm_a_dto(orm: ReservaORM, numero_mesa: int) -> Reserva:
    return Reserva(
        id=orm.id,
        fecha=date.fromisoformat(orm.fecha),
        turno=turno_desde_str(orm.turno),
        numero_mesa=numero_mesa,
        cliente=orm.cliente,
        telefono=orm.telefono,
        email=orm.email,
        personas=orm.personas,
        estado=EstadoReserva(orm.estado),
    )


def reserva_dto_a_orm(dto: Reserva, mesa_id: int, restaurant_id: int) -> ReservaORM:
    return ReservaORM(
        id=dto.id,
        restaurant_id=restaurant_id,
        fecha=dto.fecha.isoformat(),
        turno=turno_a_str(dto.turno),
        mesa_id=mesa_id,
        cliente=dto.cliente,
        telefono=dto.telefono,
        email=dto.email,
        personas=dto.personas,
        estado=dto.estado.value,
    )


def turno_config_orm_a_dict(orm: TurnoConfigORM) -> dict[str, object]:
    return {
        "turno": orm.turno,
        "activo": bool(orm.activo),
        "hora_inicio": orm.hora_inicio,
        "hora_fin": orm.hora_fin,
    }


def calendar_day_orm_a_dict(orm: CalendarDayORM) -> dict[str, object]:
    return {
        "fecha": orm.fecha,
        "cerrado": bool(orm.cerrado),
        "nota": orm.nota,
    }
