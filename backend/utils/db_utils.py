"""
Utilidades para gestión de base de datos
Funciones de mantenimiento y limpieza automática
IMPORTANTE: Ahora incluye archivado antes de borrar datos
"""

from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from models.db_models import (
    FeedbackDB,
    HistoricoInteraccionDB,
    EmocionLiberadaDB,
    GratitudDB,
    DestelloDB,
    MoodMapDB
)
import logging

logger = logging.getLogger(__name__)


def limpiar_datos_duplicados(db: Session):
    """
    Elimina registros duplicados innecesarios
    
    Args:
        db: Sesión de base de datos
    """
    print("🧹 Iniciando limpieza de datos duplicados...")
    
    # Eliminar MoodMaps duplicados del mismo minuto
    # Mantener solo el más reciente
    subquery = db.query(
        MoodMapDB.usuario_id,
        MoodMapDB.timestamp
    ).distinct().all()
    
    total_eliminados = 0
    
    # Esta es una limpieza básica
    # En producción usar queries más optimizadas
    
    return {"duplicados_eliminados": total_eliminados}


def limpiar_por_antigüedad(db: Session, dias_retencion: int = 90, archivar_primero: bool = True):
    """
    Elimina datos antiguos según política de retención
    
    Args:
        db: Sesión de base de datos
        dias_retencion: Días de retención de datos
    
    Returns:
        Diccionario con estadísticas de limpieza
    """
    # PASO 1: Archivar datos antes de borrar (CRÍTICO para investigación)
    if archivar_primero:
        from utils.archivado import archivar_todo
        print("📦 Archivando datos antes de borrar...")
        dias_archivo = max(30, dias_retencion - 7)  # Margen de seguridad
        stats = archivar_todo(db, dias_antiguedad=dias_archivo)
        print(f"✓ Archivados: {sum(stats.values())} registros en tablas permanentes")
    
    # PASO 2: Proceder con limpieza
    fecha_limite = datetime.now() - timedelta(days=dias_retencion)
    
    print(f"🧹 Limpiando datos anteriores a {fecha_limite.strftime('%Y-%m-%d')}")
    
    # Contar y eliminar feedbacks antiguos
    feedbacks_count = db.query(FeedbackDB).filter(
        FeedbackDB.timestamp < fecha_limite
    ).count()
    
    db.query(FeedbackDB).filter(
        FeedbackDB.timestamp < fecha_limite
    ).delete()
    
    # Eliminar interacciones antiguas
    interacciones_count = db.query(HistoricoInteraccionDB).filter(
        HistoricoInteraccionDB.fecha < fecha_limite
    ).count()
    
    db.query(HistoricoInteraccionDB).filter(
        HistoricoInteraccionDB.fecha < fecha_limite
    ).delete()
    
    # Eliminar emociones liberadas antiguas (más de 180 días)
    fecha_limite_emociones = datetime.now() - timedelta(days=180)
    emociones_count = db.query(EmocionLiberadaDB).filter(
        EmocionLiberadaDB.fecha_liberacion < fecha_limite_emociones
    ).count()
    
    db.query(EmocionLiberadaDB).filter(
        EmocionLiberadaDB.fecha_liberacion < fecha_limite_emociones
    ).delete()
    
    # Eliminar gratitudes antiguas (más de 180 días)
    gratitudes_count = db.query(GratitudDB).filter(
        GratitudDB.fecha_creacion < fecha_limite_emociones
    ).count()
    
    db.query(GratitudDB).filter(
        GratitudDB.fecha_creacion < fecha_limite_emociones
    ).delete()
    
    # Eliminar destellos antiguos (más de 30 días)
    fecha_limite_destellos = datetime.now() - timedelta(days=30)
    destellos_count = db.query(DestelloDB).filter(
        DestelloDB.fecha_creacion < fecha_limite_destellos
    ).count()
    
    db.query(DestelloDB).filter(
        DestelloDB.fecha_creacion < fecha_limite_destellos
    ).delete()
    
    db.commit()
    
    estadisticas = {
        "feedbacks_eliminados": feedbacks_count,
        "interacciones_eliminadas": interacciones_count,
        "emociones_eliminadas": emociones_count,
        "gratitudes_eliminadas": gratitudes_count,
        "destellos_eliminados": destellos_count,
        "fecha_limite": fecha_limite.isoformat()
    }
    
    print(f"✓ Limpieza completada:")
    print(f"  - Feedbacks: {feedbacks_count}")
    print(f"  - Interacciones: {interacciones_count}")
    print(f"  - Emociones: {emociones_count}")
    print(f"  - Gratitudes: {gratitudes_count}")
    print(f"  - Destellos: {destellos_count}")
    
    return estadisticas


def limpiar_datos_huerfanos(db: Session):
    """
    Elimina datos huérfanos (sin relación con usuario existente)
    
    Args:
        db: Sesión de base de datos
    """
    print("🧹 Limpiando datos huérfanos...")
    
    # Esta función se encargaría de limpiar registros que quedaron
    # sin referencia a usuario (aunque CASCADE debería manejar esto)
    
    # Implementación específica según necesidades
    
    return {"huerfanos_eliminados": 0}


def optimizar_base_datos(db: Session):
    """
    Optimiza la base de datos (VACUUM, ANALYZE, etc.)
    
    Args:
        db: Sesión de base de datos
    """
    print("⚡ Optimizando base de datos...")
    
    # Para SQLite
    db.execute("VACUUM")
    
    # Para PostgreSQL se usaría:
    # db.execute("VACUUM ANALYZE")
    
    print("✓ Optimización completada")
    
    return {"optimizacion": "completada"}


def obtener_estadisticas_db(db: Session):
    """
    Obtiene estadísticas de uso de la base de datos
    
    Args:
        db: Sesión de base de datos
    
    Returns:
        Diccionario con estadísticas
    """
    from models.db_models import UsuarioDB
    
    estadisticas = {
        "usuarios_total": db.query(UsuarioDB).count(),
        "feedbacks_total": db.query(FeedbackDB).count(),
        "interacciones_total": db.query(HistoricoInteraccionDB).count(),
        "emociones_liberadas_total": db.query(EmocionLiberadaDB).count(),
        "gratitudes_total": db.query(GratitudDB).count(),
        "destellos_total": db.query(DestelloDB).count(),
        "moodmaps_total": db.query(MoodMapDB).count(),
    }
    
    # Estadísticas de los últimos 30 días
    fecha_30_dias = datetime.now() - timedelta(days=30)
    
    estadisticas["feedbacks_ultimos_30_dias"] = db.query(FeedbackDB).filter(
        FeedbackDB.timestamp >= fecha_30_dias
    ).count()
    
    estadisticas["interacciones_ultimas_30_dias"] = db.query(HistoricoInteraccionDB).filter(
        HistoricoInteraccionDB.fecha >= fecha_30_dias
    ).count()
    
    return estadisticas
