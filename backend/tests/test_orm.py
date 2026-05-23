"""Pruebas del modelo ORM."""

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from reservas_app.models.orm import Base, MesaORM, RestaurantORM


def _crear_engine_con_restaurant():
    engine = create_engine("sqlite:///:memory:", future=True)
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    session = SessionLocal()
    session.add(RestaurantORM(id=1, nombre="Test"))
    session.commit()
    session.close()
    return engine, SessionLocal


def test_mesa_orm_se_persiste_y_se_recupera():
    engine, SessionLocal = _crear_engine_con_restaurant()
    session = SessionLocal()
    try:
        mesa = MesaORM(restaurant_id=1, numero=1, capacidad=4)
        session.add(mesa)
        session.commit()
        session.refresh(mesa)

        assert mesa.id is not None
        assert mesa.numero == 1
        assert mesa.capacidad == 4
        assert mesa.tenant_id is None
    finally:
        session.close()
        engine.dispose()


def test_mesa_orm_check_capacidad_positiva():
    engine, SessionLocal = _crear_engine_con_restaurant()
    session = SessionLocal()
    try:
        result = session.execute(text("SELECT sql FROM sqlite_master WHERE name='mesa'")).scalar()
        assert "capacidad_positiva" in result
    finally:
        session.close()
        engine.dispose()
