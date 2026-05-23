"""Rate limiting en memoria para endpoints públicos."""

import time
from collections import defaultdict
from threading import Lock


class InMemoryRateLimiter:
    """Ventana deslizante simple por clave (p. ej. IP del cliente)."""

    def __init__(self, max_requests: int, window_seconds: int):
        self._max_requests = max_requests
        self._window_seconds = window_seconds
        self._hits: dict[str, list[float]] = defaultdict(list)
        self._lock = Lock()

    def allow(self, key: str) -> bool:
        now = time.monotonic()
        with self._lock:
            recent = [t for t in self._hits[key] if now - t < self._window_seconds]
            if len(recent) >= self._max_requests:
                self._hits[key] = recent
                return False
            recent.append(now)
            self._hits[key] = recent
            return True

    def reset(self) -> None:
        with self._lock:
            self._hits.clear()
