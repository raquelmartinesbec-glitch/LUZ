"""
Limpieza periódica de datos menos útiles para liberar espacio.
Se ejecuta automáticamente cada mes.

Autor: Sistema Luz
Fecha: 2026-01-11
"""

from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from datetime import datetime, timedelta
from typing import Dict
import logging

from models.db_models import (
    DestelloDB, MoodMapDB, FeedbackDB, HistoricoInteraccionDB,
    EmocionLiberadaDB, GratitudDB, ConfiguracionRLDB
)

logger = logging.getLogger(__name__)


def limpiar_destellos_antiguos(db: Session, dias: int = 30) -> int:
    """
    Elimina destellos más antiguos de X días.
    Los destellos son datos visuales temporales, no críticos para investigación.
    
    Args:
        db: Sesión de base de datos
        dias: Días de retención (por defecto 30)
        
    Returns:
        Número de destellos eliminados
    """
    try:
        fecha_limite = datetime.now() - timedelta(days=dias)
        
        count = db.query(DestelloDB).filter(
            DestelloDB.fecha_creacion < fecha_limite
        ).count()
        
        db.query(DestelloDB).filter(
            DestelloDB.fecha_creacion < fecha_limite
        ).delete(synchronize_session=False)
        
        db.commit()
        logger.info(f"✓ Eliminados {count} destellos antiguos (>{dias} días)")
        return count
        
    except Exception as e:
        logger.error(f"Error limpiando destellos: {e}")
        db.rollback()
        return 0


def limpiar_moodmaps_sin_feedback(db: Session, dias: int = 60) -> int:
    """
    Elimina MoodMaps antiguos que nunca recibieron feedback.
    Sin feedback, estos datos tienen poco valor para investigación.
    
    Args:
        db: Sesión de base de datos
        dias: Días de retención (por defecto 60)
        
    Returns:
        Número de MoodMaps eliminados
    """
    try:
        fecha_limite = datetime.now() - timedelta(days=dias)
        
        # Obtener IDs de usuarios que tienen feedback
        usuarios_con_feedback = db.query(FeedbackDB.usuario_id).distinct().subquery()
        
        # MoodMaps antiguos sin feedback asociado
        count = db.query(MoodMapDB).filter(
            and_(
                MoodMapDB.timestamp < fecha_limite,
                ~MoodMapDB.usuario_id.in_(
                    db.query(FeedbackDB.usuario_id).filter(
                        FeedbackDB.timestamp >= MoodMapDB.timestamp - timedelta(hours=2),
                        FeedbackDB.timestamp <= MoodMapDB.timestamp + timedelta(hours=2)
                    )
                )
            )
        ).count()
        
        db.query(MoodMapDB).filter(
            and_(
                MoodMapDB.timestamp < fecha_limite,
                ~MoodMapDB.usuario_id.in_(
                    db.query(FeedbackDB.usuario_id).filter(
                        FeedbackDB.timestamp >= MoodMapDB.timestamp - timedelta(hours=2),
                        FeedbackDB.timestamp <= MoodMapDB.timestamp + timedelta(hours=2)
                    )
                )
            )
        ).delete(synchronize_session=False)
        
        db.commit()
        logger.info(f"✓ Eliminados {count} MoodMaps sin feedback (>{dias} días)")
        return count
        
    except Exception as e:
        logger.error(f"Error limpiando MoodMaps: {e}")
        db.rollback()
        return 0


def limpiar_interacciones_duplicadas(db: Session) -> int:
    """
    Elimina interacciones duplicadas (mismo usuario, mismo tipo, misma fecha/hora).
    Mantiene solo la más reciente de cada grupo.
    
    Returns:
        Número de duplicados eliminados
    """
    try:
        # Encontrar duplicados
        subquery = db.query(
            HistoricoInteraccionDB.usuario_id,
            HistoricoInteraccionDB.tipo,
            func.date_trunc('minute', HistoricoInteraccionDB.fecha).label('minuto'),
            func.max(HistoricoInteraccionDB.id).label('max_id')
        ).group_by(
            HistoricoInteraccionDB.usuario_id,
            HistoricoInteraccionDB.tipo,
            'minuto'
        ).having(
            func.count(HistoricoInteraccionDB.id) > 1
        ).subquery()
        
        # IDs a mantener (los más recientes)
        ids_mantener = db.query(subquery.c.max_id).all()
        ids_mantener = [id[0] for id in ids_mantener]
        
        # Contar duplicados
        duplicados = db.query(HistoricoInteraccionDB).join(
            subquery,
            and_(
                HistoricoInteraccionDB.usuario_id == subquery.c.usuario_id,
                HistoricoInteraccionDB.tipo == subquery.c.tipo,
                func.date_trunc('minute', HistoricoInteraccionDB.fecha) == subquery.c.minuto
            )
        ).filter(
            ~HistoricoInteraccionDB.id.in_(ids_mantener)
        ).count()
        
        # Eliminar duplicados
        db.query(HistoricoInteraccionDB).join(
            subquery,
            and_(
                HistoricoInteraccionDB.usuario_id == subquery.c.usuario_id,
                HistoricoInteraccionDB.tipo == subquery.c.tipo,
                func.date_trunc('minute', HistoricoInteraccionDB.fecha) == subquery.c.minuto
            )
        ).filter(
            ~HistoricoInteraccionDB.id.in_(ids_mantener)
        ).delete(synchronize_session=False)
        
        db.commit()
        logger.info(f"✓ Eliminadas {duplicados} interacciones duplicadas")
        return duplicados
        
    except Exception as e:
        logger.error(f"Error limpiando duplicados: {e}")
        db.rollback()
        return 0


def limpiar_emociones_baja_intensidad(db: Session, dias: int = 90, intensidad_minima: int = 3) -> int:
    """
    Elimina emociones liberadas antiguas de baja intensidad.
    Las emociones de baja intensidad tienen menos valor analítico.
    
    Args:
        db: Sesión de base de datos
        dias: Días de retención
        intensidad_minima: Intensidad mínima para preservar (1-10)
        
    Returns:
        Número eliminado
    """
    try:
        fecha_limite = datetime.now() - timedelta(days=dias)
        
        count = db.query(EmocionLiberadaDB).filter(
            and_(
                EmocionLiberadaDB.fecha_liberacion < fecha_limite,
                EmocionLiberadaDB.intensidad_estimada < intensidad_minima
            )
        ).count()
        
        db.query(EmocionLiberadaDB).filter(
            and_(
                EmocionLiberadaDB.fecha_liberacion < fecha_limite,
                EmocionLiberadaDB.intensidad_estimada < intensidad_minima
            )
        ).delete(synchronize_session=False)
        
        db.commit()
        logger.info(f"✓ Eliminadas {count} emociones de baja intensidad (<{intensidad_minima}, >{dias} días)")
        return count
        
    except Exception as e:
        logger.error(f"Error limpiando emociones: {e}")
        db.rollback()
        return 0


def limpiar_gratitudes_cortas(db: Session, dias: int = 120, longitud_minima: int = 10) -> int:
    """
    Elimina gratitudes antiguas muy cortas (poco contenido).
    Gratitudes de 1-2 palabras tienen menos valor para NLP.
    
    Args:
        db: Sesión de base de datos
        dias: Días de retención
        longitud_minima: Longitud mínima del texto
        
    Returns:
        Número eliminado
    """
    try:
        fecha_limite = datetime.now() - timedelta(days=dias)
        
        count = db.query(GratitudDB).filter(
            and_(
                GratitudDB.fecha_creacion < fecha_limite,
                func.length(GratitudDB.texto_gratitud) < longitud_minima
            )
        ).count()
        
        db.query(GratitudDB).filter(
            and_(
                GratitudDB.fecha_creacion < fecha_limite,
                func.length(GratitudDB.texto_gratitud) < longitud_minima
            )
        ).delete(synchronize_session=False)
        
        db.commit()
        logger.info(f"✓ Eliminadas {count} gratitudes cortas (<{longitud_minima} chars, >{dias} días)")
        return count
        
    except Exception as e:
        logger.error(f"Error limpiando gratitudes: {e}")
        db.rollback()
        return 0


def limpiar_configuraciones_rl_obsoletas(db: Session, dias: int = 180) -> int:
    """
    Elimina configuraciones de RL muy antiguas y no actualizadas.
    Si no se han actualizado en mucho tiempo, el usuario probablemente no las usa.
    
    Args:
        db: Sesión de base de datos
        dias: Días sin actualización
        
    Returns:
        Número eliminado
    """
    try:
        fecha_limite = datetime.now() - timedelta(days=dias)
        
        count = db.query(ConfiguracionRLDB).filter(
            ConfiguracionRLDB.ultima_actualizacion < fecha_limite
        ).count()
        
        db.query(ConfiguracionRLDB).filter(
            ConfiguracionRLDB.ultima_actualizacion < fecha_limite
        ).delete(synchronize_session=False)
        
        db.commit()
        logger.info(f"✓ Eliminadas {count} configuraciones RL obsoletas (>{dias} días sin actualizar)")
        return count
        
    except Exception as e:
        logger.error(f"Error limpiando configuraciones RL: {e}")
        db.rollback()
        return 0


def ejecutar_limpieza_periodica(db: Session) -> Dict[str, int]:
    """
    Ejecuta la limpieza periódica completa de datos menos útiles.
    
    Esta función se ejecuta automáticamente cada mes.
    Libera espacio eliminando datos de bajo valor analítico.
    
    Returns:
        Diccionario con conteos de eliminaciones
    """
    logger.info("\n🧹 Iniciando limpieza periódica mensual...")
    logger.info("=" * 60)
    
    resultado = {
        "destellos_antiguos": 0,
        "moodmaps_sin_feedback": 0,
        "interacciones_duplicadas": 0,
        "emociones_baja_intensidad": 0,
        "gratitudes_cortas": 0,
        "configuraciones_rl_obsoletas": 0
    }
    
    try:
        # 1. Destellos antiguos (30 días)
        resultado["destellos_antiguos"] = limpiar_destellos_antiguos(db, dias=30)
        
        # 2. MoodMaps sin feedback (60 días)
        resultado["moodmaps_sin_feedback"] = limpiar_moodmaps_sin_feedback(db, dias=60)
        
        # 3. Interacciones duplicadas
        resultado["interacciones_duplicadas"] = limpiar_interacciones_duplicadas(db)
        
        # 4. Emociones de baja intensidad (90 días, intensidad < 3)
        resultado["emociones_baja_intensidad"] = limpiar_emociones_baja_intensidad(
            db, dias=90, intensidad_minima=3
        )
        
        # 5. Gratitudes muy cortas (120 días, < 10 caracteres)
        resultado["gratitudes_cortas"] = limpiar_gratitudes_cortas(
            db, dias=120, longitud_minima=10
        )
        
        # 6. Configuraciones RL obsoletas (180 días sin actualizar)
        resultado["configuraciones_rl_obsoletas"] = limpiar_configuraciones_rl_obsoletas(
            db, dias=180
        )
        
        total = sum(resultado.values())
        
        logger.info("\n✓ Limpieza periódica completada:")
        logger.info(f"  📊 Total eliminado: {total} registros")
        logger.info(f"  - Destellos antiguos: {resultado['destellos_antiguos']}")
        logger.info(f"  - MoodMaps sin feedback: {resultado['moodmaps_sin_feedback']}")
        logger.info(f"  - Interacciones duplicadas: {resultado['interacciones_duplicadas']}")
        logger.info(f"  - Emociones baja intensidad: {resultado['emociones_baja_intensidad']}")
        logger.info(f"  - Gratitudes cortas: {resultado['gratitudes_cortas']}")
        logger.info(f"  - Configs RL obsoletas: {resultado['configuraciones_rl_obsoletas']}")
        logger.info("=" * 60)
        
        # IMPORTANTE: Archivar datos valiosos antes de la próxima limpieza
        if total > 0:
            logger.info("\n💡 Recomendación: Ejecuta /investigacion/archivar antes de la próxima limpieza")
        
        return resultado
        
    except Exception as e:
        logger.error(f"Error en limpieza periódica: {e}")
        db.rollback()
        return resultado


def obtener_estimacion_espacio_liberado(db: Session) -> Dict[str, any]:
    """
    Estima cuánto espacio se liberaría con la limpieza periódica.
    Útil para decidir si ejecutar la limpieza.
    
    Returns:
        Diccionario con estimaciones
    """
    try:
        fecha_30d = datetime.now() - timedelta(days=30)
        fecha_60d = datetime.now() - timedelta(days=60)
        fecha_90d = datetime.now() - timedelta(days=90)
        fecha_120d = datetime.now() - timedelta(days=120)
        fecha_180d = datetime.now() - timedelta(days=180)
        
        estimacion = {
            "destellos_a_eliminar": db.query(DestelloDB).filter(
                DestelloDB.fecha_creacion < fecha_30d
            ).count(),
            "moodmaps_sin_feedback": db.query(MoodMapDB).filter(
                MoodMapDB.timestamp < fecha_60d
            ).count(),  # Aproximado
            "emociones_baja_intensidad": db.query(EmocionLiberadaDB).filter(
                and_(
                    EmocionLiberadaDB.fecha_liberacion < fecha_90d,
                    EmocionLiberadaDB.intensidad_estimada < 3
                )
            ).count(),
            "gratitudes_cortas": db.query(GratitudDB).filter(
                and_(
                    GratitudDB.fecha_creacion < fecha_120d,
                    func.length(GratitudDB.texto_gratitud) < 10
                )
            ).count(),
            "configs_rl_obsoletas": db.query(ConfiguracionRLDB).filter(
                ConfiguracionRLDB.ultima_actualizacion < fecha_180d
            ).count()
        }
        
        total_estimado = sum(estimacion.values())
        espacio_mb_estimado = total_estimado * 0.0002  # ~200 bytes por registro promedio
        
        estimacion["total_registros"] = total_estimado
        estimacion["espacio_mb_estimado"] = round(espacio_mb_estimado, 2)
        
        return estimacion
        
    except Exception as e:
        logger.error(f"Error estimando espacio: {e}")
        return {}
