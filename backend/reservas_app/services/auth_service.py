"""Lógica de autenticación admin con sesiones en base de datos."""

import secrets
from datetime import datetime, timedelta, timezone

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from reservas_app.auth.passwords import hash_password, verify_password
from reservas_app.config import Configuracion
from reservas_app.exceptions import (
    CredencialesInvalidasError,
    RegistroCerradoError,
    SesionInvalidaError,
    ValorInvalidoError,
)
from reservas_app.models.orm import AdminSessionORM, AdminUserORM


class AuthService:
    """Registro del primer admin, login/logout y validación de sesiones."""

    def __init__(
        self,
        session: Session,
        config: Configuracion | None = None,
        restaurant_id: int = 1,
    ):
        self._session = session
        self._config = config or Configuracion()
        self._restaurant_id = restaurant_id

    def hay_admin_registrado(self) -> bool:
        count = self._session.scalar(select(func.count()).select_from(AdminUserORM))
        return (count or 0) > 0

    def registrar_primer_admin(self, email: str, password: str) -> tuple[AdminUserORM, str]:
        """Crea el primer admin y abre una sesión. Solo permitido si no hay admins."""
        if self.hay_admin_registrado():
            raise RegistroCerradoError("Ya existe un administrador registrado.")
        self._validar_credenciales(email, password)

        admin = AdminUserORM(
            restaurant_id=self._restaurant_id,
            email=email.strip().lower(),
            password_hash=hash_password(password),
        )
        self._session.add(admin)
        self._session.flush()
        token = self._crear_sesion(admin.id)
        self._session.commit()
        return admin, token

    def iniciar_sesion(self, email: str, password: str) -> tuple[AdminUserORM, str]:
        """Valida credenciales y devuelve admin + token de sesión."""
        self._validar_credenciales(email, password)
        admin = self._session.scalar(
            select(AdminUserORM).where(AdminUserORM.email == email.strip().lower())
        )
        if admin is None or not verify_password(password, admin.password_hash):
            raise CredencialesInvalidasError("Email o contraseña incorrectos.")
        token = self._crear_sesion(admin.id)
        self._session.commit()
        return admin, token

    def cerrar_sesion(self, token: str | None) -> None:
        if not token:
            return
        row = self._session.scalar(select(AdminSessionORM).where(AdminSessionORM.token == token))
        if row is not None:
            self._session.delete(row)
            self._session.commit()

    def admin_desde_token(self, token: str | None) -> AdminUserORM:
        if not token:
            raise SesionInvalidaError("Sesión no proporcionada.")
        row = self._session.scalar(select(AdminSessionORM).where(AdminSessionORM.token == token))
        if row is None:
            raise SesionInvalidaError("Sesión inválida.")
        if self._sesion_expirada(row.expires_at):
            self._session.delete(row)
            self._session.commit()
            raise SesionInvalidaError("La sesión expiró.")
        admin = self._session.get(AdminUserORM, row.admin_user_id)
        if admin is None:
            raise SesionInvalidaError("Usuario de sesión no encontrado.")
        return admin

    @staticmethod
    def admin_a_dict(admin: AdminUserORM) -> dict[str, object]:
        return {
            "id": admin.id,
            "email": admin.email,
            "restaurant_id": admin.restaurant_id,
        }

    def _crear_sesion(self, admin_user_id: int) -> str:
        token = secrets.token_urlsafe(32)
        expires_at = (
            datetime.now(tz=timezone.utc) + timedelta(hours=self._config.session_ttl_hours)
        ).isoformat()
        self._session.add(
            AdminSessionORM(
                token=token,
                admin_user_id=admin_user_id,
                expires_at=expires_at,
            )
        )
        return token

    @staticmethod
    def _sesion_expirada(expires_at: str) -> bool:
        try:
            limite = datetime.fromisoformat(expires_at)
        except ValueError:
            return True
        if limite.tzinfo is None:
            limite = limite.replace(tzinfo=timezone.utc)
        return datetime.now(tz=timezone.utc) >= limite

    @staticmethod
    def _validar_credenciales(email: str, password: str) -> None:
        if not email.strip():
            raise ValorInvalidoError("El email no puede estar vacío.")
        if "@" not in email or "." not in email.split("@")[-1]:
            raise ValorInvalidoError("El email no es válido.")
        if len(password) < 8:
            raise ValorInvalidoError("La contraseña debe tener al menos 8 caracteres.")
