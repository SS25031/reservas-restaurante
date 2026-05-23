"""Utilidades de contraseñas (bcrypt)."""

import bcrypt


def hash_password(password: str) -> str:
    """Genera un hash bcrypt de la contraseña en texto plano."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    """Comprueba si la contraseña coincide con el hash almacenado."""
    try:
        return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))
    except ValueError:
        return False
