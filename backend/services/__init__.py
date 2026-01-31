"""
Archivo __init__.py para el paquete services
Importaciones lazy para evitar dependencias ML automáticas
"""

# NO importar automáticamente servicios con dependencias ML pesadas
# from .ia_service import IAService  # Comentado para evitar sklearn
# from .rl_service import RLService   # Comentado para evitar deps ML
# from .nlp_service import NLPService # Comentado para evitar deps ML

# Solo hacer disponible ml_service que maneja fallbacks automáticamente
# Los otros servicios se pueden importar explícitamente cuando se necesiten

__all__ = []  # Importaciones explícitas requeridas
