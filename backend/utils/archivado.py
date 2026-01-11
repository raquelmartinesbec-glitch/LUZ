"""
Utilidades para el archivado automático de datos para investigación.
Los datos se consolidan y archivan en tablas permanentes antes de cualquier limpieza.

Autor: Sistema Luz
Fecha: 2026-01-11
"""

from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging
from collections import Counter

from models.db_models import (
    MoodMapDB, FeedbackDB, HistoricoInteraccionDB,
    EmocionLiberadaDB, GratitudDB,
    ArchivoEmocionalDB, ArchivoAlmaBoardDB, ResumenSemanalDB
)

logger = logging.getLogger(__name__)


def obtener_semana_anio(fecha: datetime) -> str:
    """
    Obtiene el string de semana-año en formato ISO: "YYYY-WXX"
    
    Args:
        fecha: Fecha a convertir
        
    Returns:
        String con formato "2026-W02"
    """
    año, semana, _ = fecha.isocalendar()
    return f"{año}-W{semana:02d}"


def obtener_mes_anio(fecha: datetime) -> str:
    """
    Obtiene el string de mes-año: "YYYY-MM"
    
    Args:
        fecha: Fecha a convertir
        
    Returns:
        String con formato "2026-01"
    """
    return f"{fecha.year}-{fecha.month:02d}"


def archivar_datos_emocionales(db: Session, dias_antiguedad: int = 30) -> int:
    """
    Archiva datos emocionales (MoodMaps + Feedbacks) en la tabla de archivo permanente.
    
    Los datos archivados NUNCA se borran automáticamente.
    Solo archiva datos que tengan al menos 'dias_antiguedad' días.
    
    Args:
        db: Sesión de base de datos
        dias_antiguedad: Solo archivar datos más antiguos que estos días
        
    Returns:
        Número de registros archivados
    """
    try:
        fecha_limite = datetime.utcnow() - timedelta(days=dias_antiguedad)
        
        # Obtener MoodMaps antiguos que no estén archivados
        moodmaps = db.query(MoodMapDB).filter(
            MoodMapDB.fecha_creacion < fecha_limite
        ).all()
        
        archivados = 0
        
        for moodmap in moodmaps:
            # Verificar si ya está archivado
            existe = db.query(ArchivoEmocionalDB).filter(
                ArchivoEmocionalDB.usuario_id == moodmap.usuario_id,
                ArchivoEmocionalDB.fecha_registro == moodmap.fecha_creacion
            ).first()
            
            if existe:
                continue
            
            # Buscar feedback asociado (si existe)
            feedback = db.query(FeedbackDB).filter(
                FeedbackDB.usuario_id == moodmap.usuario_id,
                FeedbackDB.fecha_creacion >= moodmap.fecha_creacion,
                FeedbackDB.fecha_creacion <= moodmap.fecha_creacion + timedelta(hours=2)
            ).first()
            
            # Buscar interacción asociada
            interaccion = db.query(HistoricoInteraccionDB).filter(
                HistoricoInteraccionDB.usuario_id == moodmap.usuario_id,
                HistoricoInteraccionDB.fecha >= moodmap.fecha_creacion,
                HistoricoInteraccionDB.fecha <= moodmap.fecha_creacion + timedelta(hours=2),
                HistoricoInteraccionDB.tipo == "microaccion"
            ).first()
            
            # Crear registro de archivo
            archivo = ArchivoEmocionalDB(
                usuario_id=moodmap.usuario_id,
                alegria=moodmap.alegria,
                tristeza=moodmap.tristeza,
                ansiedad=moodmap.ansiedad,
                embedding_latente=moodmap.embedding_latente,
                estado_clasificado=moodmap.estado_clasificado,
                microaccion_recomendada=interaccion.datos.get("microaccion") if interaccion and interaccion.datos else None,
                feedback_efectividad=feedback.efectividad if feedback else None,
                feedback_comodidad=feedback.comodidad if feedback else None,
                feedback_energia=feedback.energia if feedback else None,
                fecha_registro=moodmap.fecha_creacion,
                semana_anio=obtener_semana_anio(moodmap.fecha_creacion),
                datos_extra={
                    "moodmap_id": moodmap.id,
                    "feedback_id": feedback.id if feedback else None,
                    "interaccion_id": interaccion.id if interaccion else None
                }
            )
            
            db.add(archivo)
            archivados += 1
        
        db.commit()
        logger.info(f"✓ Archivados {archivados} registros emocionales")
        return archivados
        
    except Exception as e:
        logger.error(f"Error archivando datos emocionales: {e}")
        db.rollback()
        return 0


def archivar_datos_alma_board(db: Session, dias_antiguedad: int = 30) -> int:
    """
    Archiva datos del Alma Board (emociones liberadas y gratitudes).
    
    Args:
        db: Sesión de base de datos
        dias_antiguedad: Solo archivar datos más antiguos que estos días
        
    Returns:
        Número de registros archivados
    """
    try:
        fecha_limite = datetime.utcnow() - timedelta(days=dias_antiguedad)
        archivados = 0
        
        # Archivar emociones liberadas
        emociones = db.query(EmocionLiberadaDB).filter(
            EmocionLiberadaDB.fecha_liberacion < fecha_limite
        ).all()
        
        for emocion in emociones:
            # Verificar si ya está archivado
            existe = db.query(ArchivoAlmaBoardDB).filter(
                ArchivoAlmaBoardDB.usuario_id == emocion.usuario_id,
                ArchivoAlmaBoardDB.tipo == "emocion",
                ArchivoAlmaBoardDB.fecha_registro == emocion.fecha_liberacion
            ).first()
            
            if existe:
                continue
            
            archivo = ArchivoAlmaBoardDB(
                usuario_id=emocion.usuario_id,
                tipo="emocion",
                categoria=emocion.categoria,
                intensidad=emocion.intensidad,
                fecha_registro=emocion.fecha_liberacion,
                semana_anio=obtener_semana_anio(emocion.fecha_liberacion),
                mes_anio=obtener_mes_anio(emocion.fecha_liberacion),
                datos_extra={"emocion_id": emocion.id}
            )
            
            db.add(archivo)
            archivados += 1
        
        # Archivar gratitudes
        gratitudes = db.query(GratitudDB).filter(
            GratitudDB.fecha_creacion < fecha_limite
        ).all()
        
        for gratitud in gratitudes:
            # Verificar si ya está archivado
            existe = db.query(ArchivoAlmaBoardDB).filter(
                ArchivoAlmaBoardDB.usuario_id == gratitud.usuario_id,
                ArchivoAlmaBoardDB.tipo == "gratitud",
                ArchivoAlmaBoardDB.fecha_registro == gratitud.fecha_creacion
            ).first()
            
            if existe:
                continue
            
            archivo = ArchivoAlmaBoardDB(
                usuario_id=gratitud.usuario_id,
                tipo="gratitud",
                texto=gratitud.texto,
                embedding_texto=gratitud.embedding_texto,
                fecha_registro=gratitud.fecha_creacion,
                semana_anio=obtener_semana_anio(gratitud.fecha_creacion),
                mes_anio=obtener_mes_anio(gratitud.fecha_creacion),
                datos_extra={"gratitud_id": gratitud.id}
            )
            
            db.add(archivo)
            archivados += 1
        
        db.commit()
        logger.info(f"✓ Archivados {archivados} registros de Alma Board")
        return archivados
        
    except Exception as e:
        logger.error(f"Error archivando datos Alma Board: {e}")
        db.rollback()
        return 0


def generar_resumen_semanal(db: Session, usuario_id: Optional[int] = None) -> int:
    """
    Genera resúmenes semanales consolidados de datos de usuarios.
    
    Args:
        db: Sesión de base de datos
        usuario_id: ID de usuario específico, o None para todos
        
    Returns:
        Número de resúmenes generados/actualizados
    """
    try:
        # Obtener todas las semanas únicas del archivo emocional
        if usuario_id:
            semanas = db.query(
                ArchivoEmocionalDB.usuario_id,
                ArchivoEmocionalDB.semana_anio
            ).filter(
                ArchivoEmocionalDB.usuario_id == usuario_id
            ).distinct().all()
        else:
            semanas = db.query(
                ArchivoEmocionalDB.usuario_id,
                ArchivoEmocionalDB.semana_anio
            ).distinct().all()
        
        resumenes_generados = 0
        
        for usuario_id, semana_anio in semanas:
            if not semana_anio:
                continue
                
            # Extraer año y semana
            try:
                año, semana = semana_anio.split('-W')
                año = int(año)
                semana = int(semana)
            except:
                continue
            
            # Verificar si ya existe el resumen
            resumen = db.query(ResumenSemanalDB).filter(
                ResumenSemanalDB.usuario_id == usuario_id,
                ResumenSemanalDB.semana_anio == semana_anio
            ).first()
            
            if not resumen:
                resumen = ResumenSemanalDB(
                    usuario_id=usuario_id,
                    semana_anio=semana_anio,
                    anio=año,
                    semana=semana
                )
                db.add(resumen)
            
            # Calcular estadísticas de datos emocionales
            datos_emocionales = db.query(ArchivoEmocionalDB).filter(
                ArchivoEmocionalDB.usuario_id == usuario_id,
                ArchivoEmocionalDB.semana_anio == semana_anio
            ).all()
            
            if datos_emocionales:
                resumen.num_registros = len(datos_emocionales)
                resumen.alegria_promedio = sum(d.alegria for d in datos_emocionales) / len(datos_emocionales)
                resumen.tristeza_promedio = sum(d.tristeza for d in datos_emocionales) / len(datos_emocionales)
                resumen.ansiedad_promedio = sum(d.ansiedad for d in datos_emocionales) / len(datos_emocionales)
                resumen.alegria_max = max(d.alegria for d in datos_emocionales)
                resumen.tristeza_max = max(d.tristeza for d in datos_emocionales)
                resumen.ansiedad_max = max(d.ansiedad for d in datos_emocionales)
                
                # Microacciones más usadas
                microacciones = [d.microaccion_recomendada for d in datos_emocionales if d.microaccion_recomendada]
                if microacciones:
                    contador = Counter(microacciones)
                    resumen.microacciones_mas_usadas = [{"microaccion": m, "count": c} for m, c in contador.most_common(5)]
                    resumen.num_microacciones = len(microacciones)
                
                # Efectividad promedio
                efectividades = [d.feedback_efectividad for d in datos_emocionales if d.feedback_efectividad]
                if efectividades:
                    resumen.efectividad_promedio = sum(efectividades) / len(efectividades)
            
            # Estadísticas de Alma Board
            datos_alma = db.query(ArchivoAlmaBoardDB).filter(
                ArchivoAlmaBoardDB.usuario_id == usuario_id,
                ArchivoAlmaBoardDB.semana_anio == semana_anio
            ).all()
            
            if datos_alma:
                emociones = [d for d in datos_alma if d.tipo == "emocion"]
                gratitudes = [d for d in datos_alma if d.tipo == "gratitud"]
                
                resumen.num_emociones_liberadas = len(emociones)
                resumen.num_gratitudes = len(gratitudes)
                
                # Emociones más frecuentes
                if emociones:
                    categorias = [e.categoria for e in emociones if e.categoria]
                    contador = Counter(categorias)
                    resumen.emociones_mas_frecuentes = [{"categoria": c, "count": cnt} for c, cnt in contador.most_common(5)]
            
            resumen.fecha_actualizacion = datetime.utcnow()
            resumenes_generados += 1
        
        db.commit()
        logger.info(f"✓ Generados/actualizados {resumenes_generados} resúmenes semanales")
        return resumenes_generados
        
    except Exception as e:
        logger.error(f"Error generando resúmenes semanales: {e}")
        db.rollback()
        return 0


def archivar_todo(db: Session, dias_antiguedad: int = 30) -> Dict[str, int]:
    """
    Archiva todos los datos en sus tablas permanentes correspondientes.
    
    Este proceso se debe ejecutar ANTES de cualquier limpieza.
    
    Args:
        db: Sesión de base de datos
        dias_antiguedad: Solo archivar datos más antiguos que estos días
        
    Returns:
        Diccionario con conteos de registros archivados
    """
    logger.info(f"\n📦 Iniciando archivado de datos (>{dias_antiguedad} días)...")
    
    resultado = {
        "emocionales": 0,
        "alma_board": 0,
        "resumenes": 0
    }
    
    try:
        # 1. Archivar datos emocionales
        resultado["emocionales"] = archivar_datos_emocionales(db, dias_antiguedad)
        
        # 2. Archivar datos Alma Board
        resultado["alma_board"] = archivar_datos_alma_board(db, dias_antiguedad)
        
        # 3. Generar resúmenes semanales
        resultado["resumenes"] = generar_resumen_semanal(db)
        
        total = sum(resultado.values())
        logger.info(f"✓ Archivado completado: {total} registros totales")
        logger.info(f"  - Emocionales: {resultado['emocionales']}")
        logger.info(f"  - Alma Board: {resultado['alma_board']}")
        logger.info(f"  - Resúmenes: {resultado['resumenes']}")
        
        return resultado
        
    except Exception as e:
        logger.error(f"Error en archivado completo: {e}")
        return resultado


def obtener_estadisticas_archivo(db: Session) -> Dict:
    """
    Obtiene estadísticas de las tablas de archivo para investigación.
    
    Returns:
        Diccionario con estadísticas
    """
    try:
        stats = {
            "archivo_emocional": {
                "total_registros": db.query(ArchivoEmocionalDB).count(),
                "usuarios_unicos": db.query(ArchivoEmocionalDB.usuario_id).distinct().count(),
                "fecha_mas_antigua": None,
                "fecha_mas_reciente": None,
                "semanas_unicas": db.query(ArchivoEmocionalDB.semana_anio).distinct().count()
            },
            "archivo_alma_board": {
                "total_registros": db.query(ArchivoAlmaBoardDB).count(),
                "emociones": db.query(ArchivoAlmaBoardDB).filter(ArchivoAlmaBoardDB.tipo == "emocion").count(),
                "gratitudes": db.query(ArchivoAlmaBoardDB).filter(ArchivoAlmaBoardDB.tipo == "gratitud").count(),
                "usuarios_unicos": db.query(ArchivoAlmaBoardDB.usuario_id).distinct().count()
            },
            "resumenes_semanales": {
                "total_resumenes": db.query(ResumenSemanalDB).count(),
                "usuarios_unicos": db.query(ResumenSemanalDB.usuario_id).distinct().count(),
                "semanas_cubiertas": db.query(ResumenSemanalDB.semana_anio).distinct().count()
            }
        }
        
        # Fechas
        primera = db.query(ArchivoEmocionalDB).order_by(ArchivoEmocionalDB.fecha_registro).first()
        ultima = db.query(ArchivoEmocionalDB).order_by(ArchivoEmocionalDB.fecha_registro.desc()).first()
        
        if primera:
            stats["archivo_emocional"]["fecha_mas_antigua"] = primera.fecha_registro.isoformat()
        if ultima:
            stats["archivo_emocional"]["fecha_mas_reciente"] = ultima.fecha_registro.isoformat()
        
        return stats
        
    except Exception as e:
        logger.error(f"Error obteniendo estadísticas: {e}")
        return {}
