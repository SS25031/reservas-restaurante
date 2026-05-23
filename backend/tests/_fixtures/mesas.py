"""Layout fijo de 25 mesas — helper de pruebas. NO es código de producción.

El layout real vendrá de la DB en el subsistema 2; este helper existe
únicamente para que las pruebas del servicio sigan teniendo un set
representativo de mesas con el que trabajar.
"""

from reservas_app.models import Mesa


def construir_mesas() -> list[Mesa]:
    layout = [
        (range(1, 6), 2),
        (range(6, 11), 4),
        (range(11, 16), 6),
        (range(16, 21), 8),
        (range(21, 26), 10),
    ]
    return [Mesa(numero=n, capacidad=cap) for rng, cap in layout for n in rng]
