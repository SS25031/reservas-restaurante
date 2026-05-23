"""Pruebas básicas de db.py."""

from sqlalchemy import text

from reservas_app.db import SessionLocal, engine, get_db


def test_engine_existe():
    assert engine is not None


def test_session_local_produce_session_funcional():
    session = SessionLocal()
    try:
        result = session.execute(text("SELECT 1")).scalar()
        assert result == 1
    finally:
        session.close()


def test_get_db_es_iterable_y_cierra_session():
    gen = get_db()
    session = next(gen)
    assert session is not None
    result = session.execute(text("SELECT 2")).scalar()
    assert result == 2
    # Agotar el generador hace que ejecute el bloque finally que cierra la session.
    try:  # noqa: SIM105
        next(gen)
    except StopIteration:
        pass
