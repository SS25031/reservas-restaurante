"""Domain exceptions for the reservation system."""


class ReservaError(Exception):
    """Base class for all reservation domain errors."""


class ValorInvalidoError(ReservaError):
    """Caller supplied an out-of-range value (party size, date, turn, ID)."""


class CapacidadInsuficienteError(ReservaError):
    """No table in the restaurant is large enough for the requested party."""


class LimiteDiarioExcedidoError(ReservaError):
    """The requested date has reached its daily reservation cap."""


class MesaNoDisponibleError(ReservaError):
    """No suitable table is free for the requested date and turn."""


class ReservaNoEncontradaError(ReservaError):
    """No reservation matches the given ID."""


class ConflictoHorarioError(ReservaError):
    """The requested change would collide with another reservation."""


class OnboardingError(ReservaError):
    """Error en el flujo de configuración inicial del restaurante."""


class OnboardingYaCompletadoError(OnboardingError):
    """El onboarding ya fue marcado como completado."""


class OnboardingIncompletoError(OnboardingError):
    """Faltan requisitos mínimos para completar el onboarding."""
