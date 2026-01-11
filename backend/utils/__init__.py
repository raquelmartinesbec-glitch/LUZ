"""
Archivo __init__.py para el paquete utils
"""
from .db_utils import (
    limpiar_por_antigüedad,
    limpiar_datos_duplicados,
    limpiar_datos_huerfanos,
    optimizar_base_datos,
    obtener_estadisticas_db
)

__all__ = [
    'limpiar_por_antigüedad',
    'limpiar_datos_duplicados',
    'limpiar_datos_huerfanos',
    'optimizar_base_datos',
    'obtener_estadisticas_db',
]
