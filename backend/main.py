"""
Servidor principal FastAPI
App de Bienestar Interactiva - Luz
Con creación automática de tablas, limpieza periódica y archivado
"""

from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager
from typing import Optional
import uvicorn
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Importar configuración de base de datos
from database import get_db, crear_tablas

# Importar modelos
from models.usuario import MoodMap, Feedback, AlmaBoard, Destello
from models.db_models import (
    UsuarioDB, MoodMapDB, FeedbackDB, HistoricoInteraccionDB,
    EmocionLiberadaDB, GratitudDB, DestelloDB
)

# Importar servicios de IA
from services.ia_service import IAService
from services.rl_service import RLService
from services.nlp_service import NLPService

# Importar utilidades
from utils.db_utils import limpiar_por_antigüedad, optimizar_base_datos, obtener_estadisticas_db
from utils.limpieza_periodica import ejecutar_limpieza_periodica, obtener_estimacion_espacio_liberado
from utils.test_users import (
    crear_usuario_test, eliminar_usuario_test, 
    eliminar_todos_usuarios_test, listar_usuarios_test,
    verificar_es_usuario_test
)

# Scheduler global
scheduler = BackgroundScheduler()


def tarea_limpieza_mensual():
    """Tarea que se ejecuta cada mes para limpiar datos menos útiles"""
    logger.info("\n🗓️  TAREA PROGRAMADA: Limpieza mensual automática")
    db = next(get_db())
    try:
        resultado = ejecutar_limpieza_periodica(db)
        logger.info(f"✓ Limpieza mensual completada: {sum(resultado.values())} registros eliminados")
    except Exception as e:
        logger.error(f"❌ Error en limpieza mensual: {e}")
    finally:
        db.close()


# Lifecycle events
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestiona inicio y cierre del servidor"""
    # STARTUP
    print("\n🌟 Iniciando Luz - Backend de Bienestar")
    print("=" * 50)
    
    # Crear todas las tablas automáticamente
    crear_tablas()
    
    # Iniciar scheduler de limpieza periódica
    scheduler.add_job(
        tarea_limpieza_mensual,
        trigger=CronTrigger(day=1, hour=3, minute=0),  # Día 1 de cada mes a las 3:00 AM
        id='limpieza_mensual',
        name='Limpieza mensual de datos menos útiles',
        replace_existing=True
    )
    scheduler.start()
    logger.info("✓ Scheduler iniciado: Limpieza automática cada mes (día 1 a las 3:00 AM)")
    
    print("✓ Servidor listo")
    print("\n💡 NOTA: Limpieza periódica ACTIVA")
    print("   🗓️  Se ejecuta automáticamente el día 1 de cada mes")
    print("   🧹 Elimina datos menos útiles (destellos viejos, duplicados, etc.)")
    print("   📦 Los datos importantes se archivan antes de borrar")
    print("=" * 50 + "\n")
    
    yield
    
    # SHUTDOWN
    scheduler.shutdown()
    logger.info("✓ Scheduler detenido")
    print("\n👋 Cerrando servidor...")


# Crear aplicación FastAPI
app = FastAPI(
    title="Luz - API de Bienestar",
    description="API REST con IA adaptativa - Estilo boho chic zen ✨",
    version="1.0.0",
    lifespan=lifespan
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar servicios de IA
ia_service = IAService()
rl_service = RLService()
nlp_service = NLPService()


# ============================================================
# ENDPOINTS - SALUD
# ============================================================

@app.get("/")
async def root():
    """Información del servidor"""
    return {
        "nombre": "Luz - API de Bienestar",
        "version": "1.0.0",
        "estado": "activo",
        "timestamp": datetime.now().isoformat(),
        "docs": "/docs",
        "estilo": "boho chic zen ✨"
    }


@app.get("/salud")
async def verificar_salud(db: Session = Depends(get_db)):
    """Verifica estado del servidor y BD"""
    try:
        db.execute("SELECT 1")
        stats = obtener_estadisticas_db(db)
        
        return {
            "estado": "saludable",
            "base_datos": "conectada",
            "estadisticas": stats,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


# ============================================================
# ENDPOINTS - MOODMAP
# ============================================================

@app.post("/moodmap/analizar")
async def analizar_moodmap(
    moodmap: MoodMap,
    usuario_id: int = 1,
    db: Session = Depends(get_db)
):
    """Analiza estado emocional con IA"""
    try:
        # Guardar en BD
        moodmap_db = MoodMapDB(
            usuario_id=usuario_id,
            felicidad=moodmap.felicidad,
            estres=moodmap.estres,
            motivacion=moodmap.motivacion
        )
        db.add(moodmap_db)
        
        # Análisis con IA
        clasificacion = ia_service.clasificar_estado(moodmap)
        embedding = ia_service.obtener_embedding_emocional(moodmap)
        cluster_id = ia_service.obtener_cluster(moodmap)
        
        # RL: microacción adaptativa
        microaccion_rl = rl_service.obtener_microaccion_adaptativa(moodmap)
        
        # Frase motivadora
        frase = nlp_service.generar_frase_motivadora(
            moodmap,
            microaccion_rl['microaccion']
        )
        
        # Guardar interacción
        interaccion = HistoricoInteraccionDB(
            usuario_id=usuario_id,
            tipo="moodmap",
            datos=moodmap.model_dump(),
            embedding_latente=embedding.tolist(),
            cluster_id=cluster_id,
            microaccion_sugerida=microaccion_rl['microaccion']
        )
        db.add(interaccion)
        db.commit()
        
        return {
            "clasificacion": clasificacion,
            "cluster_id": cluster_id,
            "microaccion_sugerida": microaccion_rl,
            "frase_motivadora": frase,
            "embedding_dimensiones": len(embedding)
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


# ============================================================
# ENDPOINTS - FEEDBACK
# ============================================================

@app.post("/feedback/enviar")
async def enviar_feedback(feedback: Feedback, db: Session = Depends(get_db)):
    """Recibe feedback y actualiza RL"""
    try:
        # Guardar en BD
        feedback_db = FeedbackDB(
            usuario_id=feedback.usuario_id,
            microaccion=feedback.microaccion,
            efectividad=feedback.efectividad,
            comodidad=feedback.comodidad,
            energia=feedback.energia,
            comentario_texto=feedback.comentario_texto,
            moodmap_previo=feedback.moodmap_previo.model_dump(),
            moodmap_posterior=feedback.moodmap_posterior.model_dump() if feedback.moodmap_posterior else None
        )
        db.add(feedback_db)
        
        # Recompensa para RL
        recompensa = (feedback.efectividad + feedback.comodidad + feedback.energia) / 3
        
        # Actualizar RL
        rl_service.actualizar_politica(
            microaccion=feedback.microaccion,
            recompensa=recompensa,
            estado_previo=feedback.moodmap_previo,
            estado_nuevo=feedback.moodmap_posterior
        )
        
        # Análisis de sentimiento
        analisis_sentimiento = None
        if feedback.comentario_texto:
            analisis_sentimiento = nlp_service.analizar_sentimiento(feedback.comentario_texto)
        
        db.commit()
        
        return {
            "mensaje": "Feedback recibido ✨",
            "recompensa": recompensa,
            "analisis_sentimiento": analisis_sentimiento,
            "rl_actualizado": True
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


# ============================================================
# ENDPOINTS - FEEDBACK Y ANÁLISIS PREDICTIVO
# ============================================================

@app.post("/feedback/procesar-actividad")
async def procesar_actividad_completada(
    data: dict,
    db: Session = Depends(get_db)
):
    """Procesa el feedback de una actividad y calcula nuevo estado emocional"""
    try:
        tipo_actividad = data.get('tipo_actividad')
        nombre_actividad = data.get('nombre_actividad')
        intensidad = data.get('intensidad')
        notas = data.get('notas')
        usuario_id = data.get('usuario_id', 1)
        estado_anterior = data.get('estado_anterior')
        
        # Calcular nuevo estado basado en la actividad
        nuevo_estado = _calcular_impacto_actividad(
            tipo_actividad, intensidad, estado_anterior
        )
        
        # Guardar en base de datos
        feedback_db = FeedbackDB(
            usuario_id=usuario_id,
            microaccion=f"{tipo_actividad}:{nombre_actividad}",
            efectividad=min(intensidad, 5),
            comodidad=5,  # Asumir comodidad alta
            energia=intensidad,
            comentario_texto=notas
        )
        db.add(feedback_db)
        
        # Actualizar MoodMap
        moodmap_db = MoodMapDB(
            usuario_id=usuario_id,
            felicidad=nuevo_estado['felicidad'],
            estres=nuevo_estado['estres'],
            motivacion=nuevo_estado['motivacion']
        )
        db.add(moodmap_db)
        
        # Análisis predictivo para próximas sugerencias
        from models.usuario import MoodMap
        nuevo_moodmap = MoodMap(
            felicidad=nuevo_estado['felicidad'],
            estres=nuevo_estado['estres'],
            motivacion=nuevo_estado['motivacion']
        )
        
        proximas_sugerencias = ia_service.clasificar_estado(nuevo_moodmap)
        
        db.commit()
        
        return {
            "nuevo_estado": nuevo_estado,
            "mejora": {
                "felicidad": nuevo_estado['felicidad'] - estado_anterior['felicidad'],
                "estres": nuevo_estado['estres'] - estado_anterior['estres'],
                "motivacion": nuevo_estado['motivacion'] - estado_anterior['motivacion']
            },
            "proximas_sugerencias": proximas_sugerencias,
            "mensaje": f"¡Excelente! Has activado {tipo_actividad} con intensidad {intensidad}/5"
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.post("/ia/sugerencias-personalizadas")
async def obtener_sugerencias_personalizadas(
    data: dict,
    db: Session = Depends(get_db)
):
    """Obtiene sugerencias personalizadas basadas en IA y patrones de comportamiento"""
    try:
        usuario_id = data.get('usuario_id', 1)
        estado_actual = data.get('estado_actual')
        
        # Obtener historial del usuario
        historial = db.query(HistoricoInteraccionDB).filter(
            HistoricoInteraccionDB.usuario_id == usuario_id
        ).order_by(HistoricoInteraccionDB.timestamp.desc()).limit(10).all()
        
        from models.usuario import MoodMap
        moodmap = MoodMap(
            felicidad=estado_actual['felicidad'],
            estres=estado_actual['estres'],
            motivacion=estado_actual['motivacion']
        )
        
        # Análisis con IA
        clasificacion = ia_service.clasificar_estado(moodmap)
        embedding = ia_service.obtener_embedding_emocional(moodmap)
        cluster_id = ia_service.obtener_cluster(moodmap)
        
        # RL para microacciones adaptativas
        microaccion_rl = rl_service.obtener_microaccion_adaptativa(moodmap)
        
        # Convertir a natural chemicals
        natural_chemicals_sugeridos = _convertir_a_natural_chemicals(
            microaccion_rl['microaccion'], estado_actual
        )
        
        return {
            "sugerencias": natural_chemicals_sugeridos,
            "razonamiento": {
                "clasificacion_ia": clasificacion,
                "cluster_emocional": cluster_id,
                "patron_detectado": microaccion_rl['razonamiento']
            },
            "personalizacion": {
                "basado_en_historial": len(historial) > 0,
                "actividades_previas": len(historial)
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


def _calcular_impacto_actividad(tipo_actividad: str, intensidad: int, estado_anterior: dict) -> dict:
    """Calcula el impacto de una actividad en el estado emocional"""
    
    # Factores de impacto por tipo de natural chemical
    impactos = {
        'serotonina': {'felicidad': 0.15, 'estres': -0.10, 'motivacion': 0.05},
        'dopamina': {'felicidad': 0.10, 'estres': -0.05, 'motivacion': 0.20},
        'endorfinas': {'felicidad': 0.12, 'estres': -0.15, 'motivacion': 0.08},
        'oxitocina': {'felicidad': 0.18, 'estres': -0.12, 'motivacion': 0.10},
    }
    
    impacto = impactos.get(tipo_actividad, {
        'felicidad': 0.05, 'estres': -0.05, 'motivacion': 0.05
    })
    
    # Multiplicar por intensidad normalizada
    factor = intensidad / 5.0
    
    return {
        'felicidad': max(0, min(1, estado_anterior['felicidad'] + impacto['felicidad'] * factor)),
        'estres': max(0, min(1, estado_anterior['estres'] + impacto['estres'] * factor)),
        'motivacion': max(0, min(1, estado_anterior['motivacion'] + impacto['motivacion'] * factor))
    }


def _convertir_a_natural_chemicals(microaccion: str, estado_actual: dict) -> list:
    """Convierte microacciones a natural chemicals recomendados"""
    
    sugerencias = []
    
    # Análisis basado en microacción RL
    if microaccion in ['calmarse', 'meditar']:
        sugerencias.extend(['serotonina', 'endorfinas'])
    elif microaccion in ['animarse', 'motivarse']:
        sugerencias.extend(['dopamina', 'serotonina'])
    elif microaccion in ['activarse', 'ejercitarse']:
        sugerencias.extend(['dopamina', 'endorfinas'])
    elif microaccion in ['conectarse', 'socializar']:
        sugerencias.extend(['oxitocina'])
    
    # Análisis basado en estado actual
    if estado_actual.get('estres', 0) > 0.7:
        sugerencias.append('endorfinas')
    
    if estado_actual.get('motivacion', 0) < 0.4:
        sugerencias.append('dopamina')
        
    if estado_actual.get('felicidad', 0) < 0.5:
        sugerencias.append('serotonina')
    
    # Crear respuesta estructurada
    chemicals_info = []
    for chemical in list(set(sugerencias)):  # Eliminar duplicados
        chemicals_info.append({
            'tipo': chemical,
            'razon': _obtener_razon_sugerencia(chemical, estado_actual),
            'prioridad': _calcular_prioridad(chemical, estado_actual)
        })
    
    # Ordenar por prioridad
    chemicals_info.sort(key=lambda x: x['prioridad'], reverse=True)
    
    return chemicals_info


def _obtener_razon_sugerencia(chemical: str, estado: dict) -> str:
    """Obtiene la razón por la cual se sugiere un chemical específico"""
    razones = {
        'serotonina': f"Tu felicidad está en {estado.get('felicidad', 0):.1%}. La serotonina puede mejorar tu bienestar general.",
        'dopamina': f"Tu motivación está en {estado.get('motivacion', 0):.1%}. La dopamina te ayudará a sentirte más motivado.",
        'endorfinas': f"Tu estrés está en {estado.get('estres', 0):.1%}. Las endorfinas son perfectas para reducir el estrés.",
        'oxitocina': "La oxitocina fortalece las conexiones sociales y mejora tu estado de ánimo general."
    }
    return razones.get(chemical, "Recomendado para tu bienestar general.")


def _calcular_prioridad(chemical: str, estado: dict) -> float:
    """Calcula la prioridad de un chemical basado en el estado actual"""
    prioridades = {
        'serotonina': (1 - estado.get('felicidad', 0.5)) * 0.8,
        'dopamina': (1 - estado.get('motivacion', 0.5)) * 0.9,
        'endorfinas': estado.get('estres', 0.5) * 1.0,
        'oxitocina': 0.6  # Prioridad base
    }
    return prioridades.get(chemical, 0.5)


# ============================================================
# ENDPOINTS - ALMA BOARD
# ============================================================

@app.post("/alma/liberar-emocion")
async def liberar_emocion(
    emocion: str,
    usuario_id: int = 1,
    db: Session = Depends(get_db)
):
    """Registra liberación de emoción tóxica"""
    try:
        analisis = nlp_service.analizar_emocion(emocion)
        
        emocion_db = EmocionLiberadaDB(
            usuario_id=usuario_id,
            emocion=emocion,
            categoria=analisis['categoria'],
            intensidad_estimada=analisis['intensidad_estimada']
        )
        db.add(emocion_db)
        
        frase = nlp_service.generar_frase_liberacion(emocion)
        
        db.commit()
        
        return {
            "mensaje": "Emoción liberada con amor 🌊",
            "analisis": analisis,
            "frase_apoyo": frase
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.post("/alma/agregar-gratitud")
async def agregar_gratitud(
    texto_gratitud: str,
    usuario_id: int = 1,
    tipo: str = "escrito",
    db: Session = Depends(get_db)
):
    """Registra microacción de gratitud"""
    try:
        embedding = nlp_service.obtener_embeddings_texto(texto_gratitud)
        
        gratitud_db = GratitudDB(
            usuario_id=usuario_id,
            texto_gratitud=texto_gratitud,
            tipo=tipo,
            embedding_texto=embedding.tolist()
        )
        db.add(gratitud_db)
        
        frase = nlp_service.generar_frase_gratitud(texto_gratitud)
        
        db.commit()
        
        return {
            "mensaje": "Gratitud registrada ✨",
            "frase_respuesta": frase,
            "embedding_dimensiones": len(embedding)
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


# ============================================================
# ENDPOINTS - ESTADÍSTICAS
# ============================================================

@app.get("/estadisticas/{usuario_id}")
async def obtener_estadisticas_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """Obtiene estadísticas del usuario"""
    try:
        total_feedbacks = db.query(FeedbackDB).filter(FeedbackDB.usuario_id == usuario_id).count()
        total_emociones = db.query(EmocionLiberadaDB).filter(EmocionLiberadaDB.usuario_id == usuario_id).count()
        total_gratitudes = db.query(GratitudDB).filter(GratitudDB.usuario_id == usuario_id).count()
        
        stats_rl = rl_service.obtener_estadisticas()
        
        return {
            "usuario_id": usuario_id,
            "total_feedbacks": total_feedbacks,
            "emociones_liberadas": total_emociones,
            "gratitudes_registradas": total_gratitudes,
            "estadisticas_rl": stats_rl
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


# ============================================================
# ENDPOINTS - MANTENIMIENTO
# ============================================================

@app.post("/mantenimiento/limpiar")
async def ejecutar_limpieza(
    dias_retencion: int = 90,
    db: Session = Depends(get_db)
):
    """Limpia datos antiguos (admin)"""
    try:
        resultado = limpiar_por_antigüedad(db, dias_retencion)
        return {
            "mensaje": "Limpieza ejecutada 🧹",
            "resultado": resultado
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.post("/mantenimiento/optimizar")
async def ejecutar_optimizacion(db: Session = Depends(get_db)):
    """Optimiza la base de datos"""
    try:
        resultado = optimizar_base_datos(db)
        return {
            "mensaje": "Optimización completada ⚡",
            "resultado": resultado
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


# ============================================================
# ENDPOINTS DE LIMPIEZA PERIÓDICA
# ============================================================

@app.post("/mantenimiento/limpieza-periodica")
async def ejecutar_limpieza_manual(db: Session = Depends(get_db)):
    """
    Ejecuta manualmente la limpieza periódica de datos menos útiles.
    Esta misma limpieza se ejecuta automáticamente cada mes.
    """
    try:
        resultado = ejecutar_limpieza_periodica(db)
        
        return {
            "mensaje": "✅ Limpieza periódica ejecutada",
            "eliminados": resultado,
            "total": sum(resultado.values()),
            "nota": "Esta limpieza se ejecuta automáticamente cada mes"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.get("/mantenimiento/estimacion-limpieza")
async def estimar_limpieza(db: Session = Depends(get_db)):
    """
    Estima cuánto espacio se liberaría con la limpieza periódica.
    Útil para decidir si ejecutarla manualmente.
    """
    try:
        estimacion = obtener_estimacion_espacio_liberado(db)
        
        return {
            "mensaje": "Estimación de limpieza periódica",
            "estimacion": estimacion,
            "recomendacion": "Ejecuta /mantenimiento/limpieza-periodica si total > 1000 registros"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


# ============================================================
# ENDPOINTS PARA TESTS (POSTMAN)
# ============================================================

@app.post("/test/crear-usuario")
async def crear_usuario_para_test(
    nombre: str = "Usuario Test Postman",
    avatar: str = "test_avatar.png",
    tipo_test: str = "postman",
    descripcion: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Crea un usuario marcado como TEST para usar en Postman.
    Este usuario se puede eliminar completamente sin dejar rastro.
    
    Args:
        nombre: Nombre del usuario test
        avatar: Avatar del usuario
        tipo_test: Tipo de test (postman, automatico, manual)
        descripcion: Descripción del test
    
    Returns:
        Datos del usuario creado con su ID para usar en tests
    """
    try:
        resultado = crear_usuario_test(
            db, 
            nombre=nombre, 
            avatar=avatar,
            tipo_test=tipo_test,
            descripcion=descripcion
        )
        
        return {
            "mensaje": "✅ Usuario de test creado exitosamente",
            "usuario": resultado,
            "instrucciones": [
                f"1. Usa el usuario_id={resultado['usuario_id']} en tus tests de Postman",
                "2. Ejecuta todas las pruebas que necesites",
                f"3. Al terminar, elimina el usuario: DELETE /test/eliminar-usuario/{resultado['usuario_id']}",
                "4. O elimina todos los usuarios test: DELETE /test/limpiar"
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creando usuario test: {str(e)}")


@app.delete("/test/eliminar-usuario/{usuario_id}")
async def eliminar_usuario_de_test(
    usuario_id: int,
    db: Session = Depends(get_db)
):
    """
    Elimina COMPLETAMENTE un usuario de test y TODOS sus datos.
    Solo funciona con usuarios marcados como test.
    
    Args:
        usuario_id: ID del usuario test a eliminar
    
    Returns:
        Resumen de registros eliminados
    """
    try:
        resultado = eliminar_usuario_test(db, usuario_id)
        
        total = sum(resultado.values()) - resultado["usuario_id"]
        
        return {
            "mensaje": f"✅ Usuario test {usuario_id} eliminado completamente",
            "registros_eliminados": resultado,
            "total": total,
            "nota": "El usuario y TODOS sus datos han sido borrados sin dejar rastro"
        }
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error eliminando usuario test: {str(e)}")


@app.delete("/test/limpiar")
async def limpiar_todos_tests(
    tipo_test: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Elimina TODOS los usuarios de test y sus datos.
    Útil para limpiar después de una sesión de testing con Postman.
    
    Args:
        tipo_test: Si se especifica, solo elimina usuarios de ese tipo (postman, automatico, etc.)
    
    Returns:
        Resumen de limpieza
    """
    try:
        resultado = eliminar_todos_usuarios_test(db, tipo_test)
        
        return {
            "mensaje": "✅ Limpieza de tests completada",
            "resultado": resultado,
            "nota": "Todos los usuarios de test han sido eliminados sin dejar rastro"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error limpiando tests: {str(e)}")


@app.get("/test/listar")
async def listar_usuarios_de_test(db: Session = Depends(get_db)):
    """
    Lista todos los usuarios marcados como test.
    Muestra cuántos registros tiene cada uno.
    
    Returns:
        Lista de usuarios test con estadísticas
    """
    try:
        usuarios = listar_usuarios_test(db)
        
        return {
            "mensaje": "Usuarios de test activos",
            "total": len(usuarios),
            "usuarios": usuarios,
            "recomendacion": "Usa DELETE /test/limpiar para eliminar todos al terminar"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listando usuarios test: {str(e)}")


@app.get("/test/verificar/{usuario_id}")
async def verificar_usuario_test(
    usuario_id: int,
    db: Session = Depends(get_db)
):
    """
    Verifica si un usuario está marcado como test.
    
    Args:
        usuario_id: ID del usuario a verificar
    """
    try:
        es_test = verificar_es_usuario_test(db, usuario_id)
        
        return {
            "usuario_id": usuario_id,
            "es_test": es_test,
            "mensaje": "Este usuario es de test y puede eliminarse" if es_test else "Este usuario NO es de test"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error verificando usuario: {str(e)}")


# ============================================================
# ENDPOINTS DE ARCHIVO E INVESTIGACIÓN
# ============================================================

@app.post("/investigacion/archivar")
async def archivar_datos(
    dias_antiguedad: int = 30,
    db: Session = Depends(get_db)
):
    """
    Archiva datos en tablas permanentes para investigación.
    Los datos archivados NUNCA se borran automáticamente.
    
    Args:
        dias_antiguedad: Solo archivar datos más antiguos que estos días
    """
    try:
        from utils.archivado import archivar_todo
        
        resultado = archivar_todo(db, dias_antiguedad=dias_antiguedad)
        
        return {
            "mensaje": f"✅ Datos archivados para investigación",
            "dias_antiguedad": dias_antiguedad,
            "archivados": {
                "emocionales": resultado.get("emocionales", 0),
                "alma_board": resultado.get("alma_board", 0),
                "resumenes_semanales": resultado.get("resumenes", 0)
            },
            "total": sum(resultado.values()),
            "nota": "Estos datos están ahora en tablas permanentes y NO se borrarán"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error archivando: {str(e)}")


@app.get("/investigacion/estadisticas")
async def obtener_stats_investigacion(db: Session = Depends(get_db)):
    """
    Obtiene estadísticas de datos archivados para investigación.
    """
    try:
        from utils.archivado import obtener_estadisticas_archivo
        
        stats = obtener_estadisticas_archivo(db)
        
        return {
            "mensaje": "Estadísticas de archivo histórico",
            "estadisticas": stats
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.get("/investigacion/exportar/emocional")
async def exportar_datos_emocionales(
    usuario_id: Optional[int] = None,
    fecha_inicio: Optional[str] = None,
    fecha_fin: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Exporta datos emocionales archivados para investigación.
    Formato: JSON limpio listo para análisis.
    
    Args:
        usuario_id: ID de usuario específico (opcional)
        fecha_inicio: Fecha inicio en formato YYYY-MM-DD (opcional)
        fecha_fin: Fecha fin en formato YYYY-MM-DD (opcional)
    """
    try:
        from models.db_models import ArchivoEmocionalDB
        from datetime import datetime
        
        query = db.query(ArchivoEmocionalDB)
        
        if usuario_id:
            query = query.filter(ArchivoEmocionalDB.usuario_id == usuario_id)
        
        if fecha_inicio:
            fecha = datetime.fromisoformat(fecha_inicio)
            query = query.filter(ArchivoEmocionalDB.fecha_registro >= fecha)
        
        if fecha_fin:
            fecha = datetime.fromisoformat(fecha_fin)
            query = query.filter(ArchivoEmocionalDB.fecha_registro <= fecha)
        
        registros = query.order_by(ArchivoEmocionalDB.fecha_registro).all()
        
        datos = []
        for r in registros:
            datos.append({
                "id": r.id,
                "usuario_id": r.usuario_id,
                "felicidad": r.felicidad,
                "estres": r.estres,
                "motivacion": r.motivacion,
                "embedding_latente": r.embedding_latente,
                "cluster_id": r.cluster_id,
                "microaccion": r.microaccion_recomendada,
                "feedback_efectividad": r.feedback_efectividad,
                "feedback_comodidad": r.feedback_comodidad,
                "feedback_energia": r.feedback_energia,
                "fecha_registro": r.fecha_registro.isoformat(),
                "semana_anio": r.semana_anio,
                "datos_extra": r.datos_extra
            })
        
        return {
            "total_registros": len(datos),
            "filtros": {
                "usuario_id": usuario_id,
                "fecha_inicio": fecha_inicio,
                "fecha_fin": fecha_fin
            },
            "datos": datos
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.get("/investigacion/exportar/alma_board")
async def exportar_datos_alma_board(
    usuario_id: Optional[int] = None,
    tipo: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Exporta datos del Alma Board archivados.
    
    Args:
        usuario_id: ID de usuario (opcional)
        tipo: "emocion" o "gratitud" (opcional)
    """
    try:
        from models.db_models import ArchivoAlmaBoardDB
        
        query = db.query(ArchivoAlmaBoardDB)
        
        if usuario_id:
            query = query.filter(ArchivoAlmaBoardDB.usuario_id == usuario_id)
        
        if tipo:
            query = query.filter(ArchivoAlmaBoardDB.tipo == tipo)
        
        registros = query.order_by(ArchivoAlmaBoardDB.fecha_registro).all()
        
        datos = []
        for r in registros:
            datos.append({
                "id": r.id,
                "usuario_id": r.usuario_id,
                "tipo": r.tipo,
                "emocion": r.emocion,
                "categoria": r.categoria,
                "intensidad": r.intensidad,
                "texto": r.texto,
                "embedding_texto": r.embedding_texto,
                "fecha_registro": r.fecha_registro.isoformat(),
                "semana_anio": r.semana_anio,
                "mes_anio": r.mes_anio,
                "datos_extra": r.datos_extra
            })
        
        return {
            "total_registros": len(datos),
            "filtros": {
                "usuario_id": usuario_id,
                "tipo": tipo
            },
            "datos": datos
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.get("/investigacion/resumenes_semanales")
async def obtener_resumenes_semanales(
    usuario_id: Optional[int] = None,
    anio: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    Obtiene resúmenes semanales consolidados para análisis.
    """
    try:
        from models.db_models import ResumenSemanalDB
        
        query = db.query(ResumenSemanalDB)
        
        if usuario_id:
            query = query.filter(ResumenSemanalDB.usuario_id == usuario_id)
        
        if anio:
            query = query.filter(ResumenSemanalDB.anio == anio)
        
        resumenes = query.order_by(
            ResumenSemanalDB.anio,
            ResumenSemanalDB.semana
        ).all()
        
        datos = []
        for r in resumenes:
            datos.append({
                "semana_anio": r.semana_anio,
                "usuario_id": r.usuario_id,
                "num_registros": r.num_registros,
                "emociones": {
                    "felicidad_promedio": r.felicidad_promedio,
                    "estres_promedio": r.estres_promedio,
                    "motivacion_promedio": r.motivacion_promedio,
                    "felicidad_max": r.felicidad_max,
                    "estres_max": r.estres_max,
                    "motivacion_max": r.motivacion_max
                },
                "microacciones": {
                    "total": r.num_microacciones,
                    "mas_usadas": r.microacciones_mas_usadas,
                    "efectividad_promedio": r.efectividad_promedio
                },
                "alma_board": {
                    "emociones_liberadas": r.num_emociones_liberadas,
                    "gratitudes": r.num_gratitudes,
                    "emociones_frecuentes": r.emociones_mas_frecuentes
                }
            })
        
        return {
            "total_semanas": len(datos),
            "filtros": {
                "usuario_id": usuario_id,
                "anio": anio
            },
            "resumenes": datos
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


# ============================================================
# EJECUTAR SERVIDOR
# ============================================================

if __name__ == "__main__":
    print("\n🌟 Luz - Backend de Bienestar")
    print("📚 Docs: http://localhost:8000/docs\n")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
