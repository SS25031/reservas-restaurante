"""Lógica de negocio del onboarding inicial del restaurante."""

from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from reservas_app.exceptions import (
    OnboardingIncompletoError,
    OnboardingYaCompletadoError,
    ValorInvalidoError,
)
from reservas_app.models import Mesa, Turno
from reservas_app.models.mappers import (
    calendar_day_orm_a_dict,
    turno_config_orm_a_dict,
)
from reservas_app.models.orm import CalendarDayORM, RestaurantORM, TurnoConfigORM
from reservas_app.repositories.mesa_repo import SqlAlchemyMesaRepository


class OnboardingService:
    """Orquesta la configuración inicial del restaurante (sin capa HTTP)."""

    def __init__(self, session: Session, restaurant_id: int = 1):
        self._session = session
        self._restaurant_id = restaurant_id
        self._mesa_repo = SqlAlchemyMesaRepository(session, restaurant_id)

    def _restaurant(self) -> RestaurantORM:
        restaurant = self._session.get(RestaurantORM, self._restaurant_id)
        if restaurant is None:
            msg = f"No existe restaurant con id {self._restaurant_id}."
            raise ValorInvalidoError(msg)
        return restaurant

    def obtener_estado(self) -> dict[str, object]:
        restaurant = self._restaurant()
        activos = len(
            self._session.scalars(
                select(TurnoConfigORM).where(
                    TurnoConfigORM.restaurant_id == self._restaurant_id,
                    TurnoConfigORM.activo.is_(True),
                )
            ).all()
        )
        return {
            "completado": bool(restaurant.onboarding_completado),
            "mesas_count": self._mesa_repo.contar(),
            "turnos_activos": activos,
        }

    def obtener_restaurant(self) -> dict[str, object]:
        restaurant = self._restaurant()
        return {
            "id": restaurant.id,
            "nombre": restaurant.nombre,
            "max_reservas_por_dia": restaurant.max_reservas_por_dia,
            "capacidad_maxima_grupo": restaurant.capacidad_maxima_grupo,
            "onboarding_completado": bool(restaurant.onboarding_completado),
        }

    def actualizar_restaurant(
        self,
        *,
        nombre: str | None = None,
        max_reservas_por_dia: int | None = None,
        capacidad_maxima_grupo: int | None = None,
    ) -> dict[str, object]:
        restaurant = self._restaurant()
        if nombre is not None:
            if not nombre.strip():
                raise ValorInvalidoError("El nombre del restaurante no puede estar vacío.")
            restaurant.nombre = nombre.strip()
        if max_reservas_por_dia is not None:
            if max_reservas_por_dia < 1:
                raise ValorInvalidoError("max_reservas_por_dia debe ser ≥ 1.")
            restaurant.max_reservas_por_dia = max_reservas_por_dia
        if capacidad_maxima_grupo is not None:
            if capacidad_maxima_grupo < 1:
                raise ValorInvalidoError("capacidad_maxima_grupo debe ser ≥ 1.")
            restaurant.capacidad_maxima_grupo = capacidad_maxima_grupo
        self._session.commit()
        return self.obtener_restaurant()

    def listar_mesas(self) -> list[dict[str, object]]:
        return [self._mesa_a_dict(m) for m in self._mesa_repo.listar()]

    def guardar_mesas(self, mesas: list[Mesa]) -> list[dict[str, object]]:
        self._validar_mesas(mesas)
        self._mesa_repo.reemplazar_todas(mesas)
        return self.listar_mesas()

    def listar_turnos(self) -> list[dict[str, object]]:
        stmt = (
            select(TurnoConfigORM)
            .where(TurnoConfigORM.restaurant_id == self._restaurant_id)
            .order_by(TurnoConfigORM.turno)
        )
        return [turno_config_orm_a_dict(row) for row in self._session.scalars(stmt)]

    def guardar_turnos(self, turnos: list[dict[str, object]]) -> list[dict[str, object]]:
        for item in turnos:
            turno_nombre = str(item["turno"])
            if turno_nombre not in {t.name for t in Turno}:
                raise ValorInvalidoError(f"Turno inválido: {turno_nombre}.")
            stmt = select(TurnoConfigORM).where(
                TurnoConfigORM.restaurant_id == self._restaurant_id,
                TurnoConfigORM.turno == turno_nombre,
            )
            config = self._session.scalar(stmt)
            if config is None:
                config = TurnoConfigORM(
                    restaurant_id=self._restaurant_id,
                    turno=turno_nombre,
                )
                self._session.add(config)
            config.activo = bool(item.get("activo", True))
            config.hora_inicio = item.get("hora_inicio")  # type: ignore[assignment]
            config.hora_fin = item.get("hora_fin")  # type: ignore[assignment]
        self._session.commit()
        return self.listar_turnos()

    def listar_calendario(
        self, *, desde: date | None = None, hasta: date | None = None
    ) -> list[dict[str, object]]:
        stmt = select(CalendarDayORM).where(CalendarDayORM.restaurant_id == self._restaurant_id)
        if desde is not None:
            stmt = stmt.where(CalendarDayORM.fecha >= desde.isoformat())
        if hasta is not None:
            stmt = stmt.where(CalendarDayORM.fecha <= hasta.isoformat())
        stmt = stmt.order_by(CalendarDayORM.fecha)
        return [calendar_day_orm_a_dict(row) for row in self._session.scalars(stmt)]

    def guardar_calendario(self, dias: list[dict[str, object]]) -> list[dict[str, object]]:
        fechas_vistas: set[str] = set()
        for item in dias:
            fecha_str = str(item["fecha"])
            if fecha_str in fechas_vistas:
                raise ValorInvalidoError(f"Fecha duplicada en el payload: {fecha_str}.")
            fechas_vistas.add(fecha_str)
            stmt = select(CalendarDayORM).where(
                CalendarDayORM.restaurant_id == self._restaurant_id,
                CalendarDayORM.fecha == fecha_str,
            )
            row = self._session.scalar(stmt)
            cerrado = bool(item.get("cerrado", False))
            nota = item.get("nota")
            if row is None:
                row = CalendarDayORM(
                    restaurant_id=self._restaurant_id,
                    fecha=fecha_str,
                )
                self._session.add(row)
            if not cerrado and not nota:
                if row.id is not None:
                    self._session.delete(row)
                continue
            row.cerrado = cerrado
            row.nota = str(nota) if nota is not None else None
        self._session.commit()
        return self.listar_calendario()

    def completar_onboarding(self) -> dict[str, bool]:
        restaurant = self._restaurant()
        if restaurant.onboarding_completado:
            raise OnboardingYaCompletadoError("El onboarding ya está completado.")
        if self._mesa_repo.contar() < 1:
            raise OnboardingIncompletoError("Se requiere al menos una mesa.")
        activos = len(
            self._session.scalars(
                select(TurnoConfigORM).where(
                    TurnoConfigORM.restaurant_id == self._restaurant_id,
                    TurnoConfigORM.activo.is_(True),
                )
            ).all()
        )
        if activos < 1:
            raise OnboardingIncompletoError("Se requiere al menos un turno activo.")
        restaurant.onboarding_completado = True
        self._session.commit()
        return {"completado": True}

    @staticmethod
    def _mesa_a_dict(mesa: Mesa) -> dict[str, object]:
        return {
            "numero": mesa.numero,
            "capacidad": mesa.capacidad,
            "pos_x": mesa.pos_x,
            "pos_y": mesa.pos_y,
        }

    @staticmethod
    def _validar_mesas(mesas: list[Mesa]) -> None:
        if not mesas:
            raise ValorInvalidoError("Se requiere al menos una mesa.")
        numeros = [m.numero for m in mesas]
        if len(numeros) != len(set(numeros)):
            raise ValorInvalidoError("Los números de mesa deben ser únicos.")
        for mesa in mesas:
            if mesa.capacidad < 1:
                raise ValorInvalidoError(f"La mesa {mesa.numero} debe tener capacidad ≥ 1.")
