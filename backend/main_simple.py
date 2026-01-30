"""
Servidor principal FastAPI - Versión simplificada
App de Bienestar Interactiva - Luz
Sin IA/ML pesado para inicio rápido
"""

from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager
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

# Importar utilidades
from utils.db_utils import limpiar_por_antigüedad, optimizar_base_datos, obtener_estadisticas_db
from utils.limpieza_periodica import ejecutar_limpieza_periodica, obtener_estimacion_espacio_liberado
from utils.test_users import (
    crear_usuario_test, eliminar_usuario_test, 
    listar_usuarios_test
)

# Scheduler para tareas programadas
scheduler = BackgroundScheduler()


def tarea_limpieza_mensual():
    """Tarea que se ejecuta el día 1 de cada mes para limpieza"""
    try:
        db = next(get_db())
        resultado = ejecutar_limpieza_periodica(db)
        logger.info(f"Limpieza mensual completada: {resultado}")
    except Exception as e:
        logger.error(f"Error en limpieza mensual: {e}")


# Lifecycle events
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestiona inicio y cierre del servidor"""
    # STARTUP
    print("\n🌟 Iniciando Luz - Backend de Bienestar (Versión Simplificada)")
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
    print("✓ Scheduler iniciado")
    print("✓ Servidor listo para recibir conexiones")
    print("📡 API: http://localhost:8000")
    print("📖 Docs: http://localhost:8000/docs")
    
    yield
    
    # SHUTDOWN
    print("\n🔄 Cerrando servidor...")
    scheduler.shutdown()
    print("✓ Scheduler detenido")


# Crear aplicación FastAPI
app = FastAPI(
    title="Luz - Bienestar Interactivo",
    description="API backend para app de bienestar con MoodMap, Alma Board y microacciones",
    version="1.0.0",
    lifespan=lifespan
)

# Configurar CORS para permitir conexiones desde Flutter
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Flutter web
        "http://127.0.0.1:3000",
        "http://localhost:8080",
        "http://127.0.0.1:8080",
        "*"  # Para desarrollo - restringir en producción
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ===== ENDPOINTS BÁSICOS =====

@app.get("/")
async def raiz():
    """Endpoint de bienvenida"""
    return {
        "mensaje": "🌟 Luz - API de Bienestar Interactivo",
        "version": "1.0.0",
        "status": "activo",
        "documentacion": "/docs",
        "features": [
            "Gestión de usuarios",
            "MoodMap tracking",
            "Alma Board (liberación y gratitud)",
            "Sistema de feedback",
            "Destellos personalizables"
        ]
    }


@app.get("/health")
async def health_check():
    """Health check para monitoreo"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }


# ===== GESTIÓN DE USUARIOS =====

@app.post("/usuarios/", response_model=dict)
async def crear_usuario(nombre: str, avatar: str = "default.png", db: Session = Depends(get_db)):
    """Crear un nuevo usuario"""
    try:
        usuario = UsuarioDB(nombre=nombre, avatar=avatar)
        db.add(usuario)
        db.commit()
        db.refresh(usuario)
        
        return {
            "id": usuario.id,
            "nombre": usuario.nombre,
            "avatar": usuario.avatar,
            "fecha_creacion": usuario.fecha_creacion.isoformat(),
            "mensaje": "Usuario creado exitosamente"
        }
    except Exception as e:
        logger.error(f"Error creando usuario: {e}")
        raise HTTPException(status_code=500, detail=f"Error creando usuario: {e}")


@app.get("/usuarios/")
async def listar_usuarios(db: Session = Depends(get_db)):
    """Listar todos los usuarios"""
    try:
        usuarios = db.query(UsuarioDB).all()
        return {
            "usuarios": [
                {
                    "id": u.id,
                    "nombre": u.nombre,
                    "avatar": u.avatar,
                    "fecha_creacion": u.fecha_creacion.isoformat()
                }
                for u in usuarios
            ],
            "total": len(usuarios)
        }
    except Exception as e:
        logger.error(f"Error listando usuarios: {e}")
        raise HTTPException(status_code=500, detail=f"Error listando usuarios: {e}")


@app.get("/usuarios/{usuario_id}")
async def obtener_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """Obtener información de un usuario específico"""
    try:
        usuario = db.query(UsuarioDB).filter(UsuarioDB.id == usuario_id).first()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        return {
            "id": usuario.id,
            "nombre": usuario.nombre,
            "avatar": usuario.avatar,
            "fecha_creacion": usuario.fecha_creacion.isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error obteniendo usuario {usuario_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Error obteniendo usuario: {e}")


# ===== MOODMAP =====

@app.post("/moodmap/")
async def crear_moodmap(moodmap: MoodMap, db: Session = Depends(get_db)):
    """Crear entrada en MoodMap"""
    try:
        # Verificar que el usuario existe
        usuario = db.query(UsuarioDB).filter(UsuarioDB.id == moodmap.usuario_id).first()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        # Crear entrada en MoodMap
        moodmap_db = MoodMapDB(
            usuario_id=moodmap.usuario_id,
            emociones=",".join(moodmap.emociones),
            intensidad=moodmap.intensidad,
            notas=moodmap.notas
        )
        db.add(moodmap_db)
        db.commit()
        db.refresh(moodmap_db)
        
        return {
            "id": moodmap_db.id,
            "usuario_id": moodmap_db.usuario_id,
            "emociones": moodmap_db.emociones.split(","),
            "intensidad": moodmap_db.intensidad,
            "notas": moodmap_db.notas,
            "timestamp": moodmap_db.timestamp.isoformat(),
            "mensaje": "MoodMap registrado exitosamente"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creando MoodMap: {e}")
        raise HTTPException(status_code=500, detail=f"Error creando MoodMap: {e}")


@app.get("/moodmap/{usuario_id}")
async def obtener_moodmaps(usuario_id: int, limit: int = 10, db: Session = Depends(get_db)):
    """Obtener MoodMaps de un usuario"""
    try:
        moodmaps = db.query(MoodMapDB).filter(
            MoodMapDB.usuario_id == usuario_id
        ).order_by(MoodMapDB.timestamp.desc()).limit(limit).all()
        
        return {
            "moodmaps": [
                {
                    "id": mm.id,
                    "emociones": mm.emociones.split(",") if mm.emociones else [],
                    "intensidad": mm.intensidad,
                    "notas": mm.notas,
                    "timestamp": mm.timestamp.isoformat()
                }
                for mm in moodmaps
            ],
            "total": len(moodmaps),
            "usuario_id": usuario_id
        }
    except Exception as e:
        logger.error(f"Error obteniendo MoodMaps para usuario {usuario_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Error obteniendo MoodMaps: {e}")


# ===== ALMA BOARD =====

@app.post("/alma-board/liberar")
async def liberar_emocion(alma_board: AlmaBoard, db: Session = Depends(get_db)):
    """Liberar una emoción tóxica"""
    try:
        # Verificar que el usuario existe
        usuario = db.query(UsuarioDB).filter(UsuarioDB.id == alma_board.usuario_id).first()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        # Crear liberación de emoción
        liberacion = EmocionLiberadaDB(
            usuario_id=alma_board.usuario_id,
            emocion_toxica=alma_board.emocion_toxica,
            descripcion=alma_board.descripcion
        )
        db.add(liberacion)
        db.commit()
        db.refresh(liberacion)
        
        return {
            "id": liberacion.id,
            "usuario_id": liberacion.usuario_id,
            "emocion_toxica": liberacion.emocion_toxica,
            "descripcion": liberacion.descripcion,
            "timestamp": liberacion.timestamp.isoformat(),
            "mensaje": "Emoción liberada exitosamente"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error liberando emoción: {e}")
        raise HTTPException(status_code=500, detail=f"Error liberando emoción: {e}")


@app.post("/alma-board/gratitud")
async def expresar_gratitud(alma_board: AlmaBoard, db: Session = Depends(get_db)):
    """Expresar gratitud"""
    try:
        # Verificar que el usuario existe
        usuario = db.query(UsuarioDB).filter(UsuarioDB.id == alma_board.usuario_id).first()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        # Crear expresión de gratitud
        gratitud = GratitudDB(
            usuario_id=alma_board.usuario_id,
            mensaje_gratitud=alma_board.mensaje_gratitud,
            categoria=alma_board.categoria
        )
        db.add(gratitud)
        db.commit()
        db.refresh(gratitud)
        
        return {
            "id": gratitud.id,
            "usuario_id": gratitud.usuario_id,
            "mensaje_gratitud": gratitud.mensaje_gratitud,
            "categoria": gratitud.categoria,
            "timestamp": gratitud.timestamp.isoformat(),
            "mensaje": "Gratitud expresada exitosamente"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error expresando gratitud: {e}")
        raise HTTPException(status_code=500, detail=f"Error expresando gratitud: {e}")


# ===== FEEDBACK =====

@app.post("/feedback/")
async def enviar_feedback(feedback: Feedback, db: Session = Depends(get_db)):
    """Enviar feedback del usuario"""
    try:
        # Verificar que el usuario existe
        usuario = db.query(UsuarioDB).filter(UsuarioDB.id == feedback.usuario_id).first()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        # Crear feedback
        feedback_db = FeedbackDB(
            usuario_id=feedback.usuario_id,
            utilidad=feedback.utilidad,
            facilidad_uso=feedback.facilidad_uso,
            probabilidad_recomendacion=feedback.probabilidad_recomendacion,
            comentarios=feedback.comentarios
        )
        db.add(feedback_db)
        db.commit()
        db.refresh(feedback_db)
        
        return {
            "id": feedback_db.id,
            "usuario_id": feedback_db.usuario_id,
            "utilidad": feedback_db.utilidad,
            "facilidad_uso": feedback_db.facilidad_uso,
            "probabilidad_recomendacion": feedback_db.probabilidad_recomendacion,
            "comentarios": feedback_db.comentarios,
            "timestamp": feedback_db.timestamp.isoformat(),
            "mensaje": "Feedback registrado exitosamente"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error registrando feedback: {e}")
        raise HTTPException(status_code=500, detail=f"Error registrando feedback: {e}")


# ===== DESTELLOS =====

@app.post("/destellos/")
async def crear_destello(destello: Destello, db: Session = Depends(get_db)):
    """Crear un destello personalizable"""
    try:
        # Verificar que el usuario existe
        usuario = db.query(UsuarioDB).filter(UsuarioDB.id == destello.usuario_id).first()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        # Crear destello
        destello_db = DestelloDB(
            usuario_id=destello.usuario_id,
            mensaje=destello.mensaje,
            tipo=destello.tipo,
            color=destello.color,
            duracion_ms=destello.duracion_ms
        )
        db.add(destello_db)
        db.commit()
        db.refresh(destello_db)
        
        return {
            "id": destello_db.id,
            "usuario_id": destello_db.usuario_id,
            "mensaje": destello_db.mensaje,
            "tipo": destello_db.tipo,
            "color": destello_db.color,
            "duracion_ms": destello_db.duracion_ms,
            "timestamp": destello_db.timestamp.isoformat(),
            "mensaje_respuesta": "Destello creado exitosamente"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creando destello: {e}")
        raise HTTPException(status_code=500, detail=f"Error creando destello: {e}")


# ===== USUARIOS DE TEST =====

@app.post("/test/usuarios/")
async def crear_usuario_de_prueba(
    nombre: str = "Usuario Test API",
    avatar: str = "test_api.png",
    tipo_test: str = "api",
    db: Session = Depends(get_db)
):
    """Crear usuario de prueba para testing"""
    try:
        resultado = crear_usuario_test(
            db=db,
            nombre=nombre,
            avatar=avatar,
            tipo_test=tipo_test,
            descripcion=f"Usuario de test {tipo_test} creado via API"
        )
        return resultado
    except Exception as e:
        logger.error(f"Error creando usuario test: {e}")
        raise HTTPException(status_code=500, detail=f"Error creando usuario test: {e}")


@app.get("/test/usuarios/")
async def obtener_usuarios_test(db: Session = Depends(get_db)):
    """Listar todos los usuarios de test"""
    try:
        usuarios = listar_usuarios_test(db)
        return usuarios
    except Exception as e:
        logger.error(f"Error listando usuarios test: {e}")
        raise HTTPException(status_code=500, detail=f"Error listando usuarios test: {e}")


@app.delete("/test/usuarios/{usuario_id}")
async def eliminar_usuario_de_prueba(usuario_id: int, db: Session = Depends(get_db)):
    """Eliminar usuario de prueba completamente"""
    try:
        resultado = eliminar_usuario_test(db, usuario_id)
        return resultado
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error eliminando usuario test {usuario_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Error eliminando usuario test: {e}")


# ===== UTILIDADES DE ADMINISTRACIÓN =====

@app.get("/admin/stats")
async def obtener_estadisticas(db: Session = Depends(get_db)):
    """Obtener estadísticas de la base de datos"""
    try:
        stats = obtener_estadisticas_db(db)
        return stats
    except Exception as e:
        logger.error(f"Error obteniendo estadísticas: {e}")
        raise HTTPException(status_code=500, detail=f"Error obteniendo estadísticas: {e}")


if __name__ == "__main__":
    uvicorn.run(
        "main_simple:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )