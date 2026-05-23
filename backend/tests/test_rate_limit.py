"""Pruebas del rate limiter en memoria."""

from reservas_app.api.rate_limit import InMemoryRateLimiter


def test_allow_hasta_el_limite():
    limiter = InMemoryRateLimiter(max_requests=2, window_seconds=60)
    assert limiter.allow("1.2.3.4") is True
    assert limiter.allow("1.2.3.4") is True
    assert limiter.allow("1.2.3.4") is False


def test_claves_independientes():
    limiter = InMemoryRateLimiter(max_requests=1, window_seconds=60)
    assert limiter.allow("a") is True
    assert limiter.allow("b") is True
    assert limiter.allow("a") is False
