"""Repositorio de reservas respaldado por SQLAlchemy.

Cumple el Protocol `ReservaRepository`. La implementación real de `cargar`
y `guardar` llega en el subsistema 2 cuando exista `ReservaORM`. Por
ahora ambos métodos levantan NotImplementedError para que cualquier
intento de usarlo prematuramente falle ruidosamente.
"""

from sqlalchemy.orm import Session

from reservas_app.models import Reserva


class SqlAlchemyReservaRepository:
    """Persistencia de reservas vía SQLAlchemy.

    Se construye con una Session ya abierta — la gestión de su ciclo de
    vida (commit/rollback/close) es responsabilidad de quien la crea
    (en producción: `get_db()` en `db.py`; en tests: fixture `db_session`).
    """

    def __init__(self, session: Session):
        self._session = session

    def cargar(self) -> tuple[list[Reserva], int]:
        raise NotImplementedError(
            "SqlAlchemyReservaRepository.cargar se implementa en el subsistema 2 "
            "(requiere ReservaORM)."
        )

    def guardar(self, reservas: list[Reserva], ultimo_id: int) -> None:
        raise NotImplementedError(
            "SqlAlchemyReservaRepository.guardar se implementa en el subsistema 2 "
            "(requiere ReservaORM)."
        )
