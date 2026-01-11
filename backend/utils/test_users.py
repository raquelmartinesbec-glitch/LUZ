"""
Utilidades para gestión de usuarios de test (Postman, etc.)
Permite crear usuarios temporales que se pueden eliminar sin dejar rastro.

Autor: Sistema Luz
Fecha: 2026-01-11
"""

from sqlalchemy.orm import Session
from datetime import datetime
from typing import Dict, List, Optional
import logging

from models.db_models import (
    UsuarioDB, UsuarioTestDB, MoodMapDB, FeedbackDB, 
    HistoricoInteraccionDB, EmocionLiberadaDB, GratitudDB, 
    DestelloDB, ConfiguracionRLDB
)

logger = logging.getLogger(__name__)


def crear_usuario_test(
    db: Session, 
    nombre: str = "Usuario Test Postman",
    avatar: str = "test_avatar.png",
    tipo_test: str = "postman",
    descripcion: Optional[str] = None
) -> Dict:
    """
    Crea un usuario marcado como test.
    Estos usuarios se pueden eliminar completamente sin dejar rastro.
    
    Args:
        db: Sesión de base de datos
        nombre: Nombre del usuario
        avatar: Avatar del usuario
        tipo_test: Tipo de test (postman, automatico, manual)
        descripcion: Descripción opcional del test
        
    Returns:
        Diccionario con datos del usuario creado
    """
    try:
        # Crear usuario normal
        usuario = UsuarioDB(
            nombre=nombre,
            avatar=avatar
        )
        db.add(usuario)
        db.flush()  # Para obtener el ID
        
        # Marcar como usuario de test
        usuario_test = UsuarioTestDB(
            usuario_id=usuario.id,
            tipo_test=tipo_test,
            descripcion=descripcion or f"Test {tipo_test} creado el {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        )
        db.add(usuario_test)
        db.commit()
        
        logger.info(f"✓ Usuario test creado: ID={usuario.id}, nombre={nombre}")
        
        return {
            "usuario_id": usuario.id,
            "nombre": usuario.nombre,
            "avatar": usuario.avatar,
            "tipo_test": tipo_test,
            "fecha_creacion": usuario.fecha_creacion.isoformat(),
            "descripcion": usuario_test.descripcion,
            "mensaje": "Usuario de test creado. Usa este ID para tus pruebas de Postman."
        }
        
    except Exception as e:
        logger.error(f"Error creando usuario test: {e}")
        db.rollback()
        raise


def eliminar_usuario_test(db: Session, usuario_id: int) -> Dict[str, int]:
    """
    Elimina completamente un usuario de test y TODOS sus datos.
    Borra de todas las tablas sin dejar rastro.
    
    Args:
        db: Sesión de base de datos
        usuario_id: ID del usuario a eliminar
        
    Returns:
        Diccionario con conteo de registros eliminados por tabla
    """
    try:
        # Verificar que sea un usuario de test
        usuario_test = db.query(UsuarioTestDB).filter(
            UsuarioTestDB.usuario_id == usuario_id
        ).first()
        
        if not usuario_test:
            raise ValueError(f"El usuario {usuario_id} NO es un usuario de test. Solo se pueden eliminar usuarios marcados como test.")
        
        resultado = {
            "usuario_id": usuario_id,
            "moodmaps": 0,
            "feedbacks": 0,
            "interacciones": 0,
            "emociones_liberadas": 0,
            "gratitudes": 0,
            "destellos": 0,
            "configuraciones_rl": 0,
            "usuario": 0,
            "registro_test": 0
        }
        
        # Eliminar de todas las tablas (orden importante para foreign keys)
        
        # 1. MoodMaps
        resultado["moodmaps"] = db.query(MoodMapDB).filter(
            MoodMapDB.usuario_id == usuario_id
        ).delete(synchronize_session=False)
        
        # 2. Feedbacks
        resultado["feedbacks"] = db.query(FeedbackDB).filter(
            FeedbackDB.usuario_id == usuario_id
        ).delete(synchronize_session=False)
        
        # 3. Histórico de interacciones
        resultado["interacciones"] = db.query(HistoricoInteraccionDB).filter(
            HistoricoInteraccionDB.usuario_id == usuario_id
        ).delete(synchronize_session=False)
        
        # 4. Emociones liberadas
        resultado["emociones_liberadas"] = db.query(EmocionLiberadaDB).filter(
            EmocionLiberadaDB.usuario_id == usuario_id
        ).delete(synchronize_session=False)
        
        # 5. Gratitudes
        resultado["gratitudes"] = db.query(GratitudDB).filter(
            GratitudDB.usuario_id == usuario_id
        ).delete(synchronize_session=False)
        
        # 6. Destellos
        resultado["destellos"] = db.query(DestelloDB).filter(
            DestelloDB.usuario_id == usuario_id
        ).delete(synchronize_session=False)
        
        # 7. Configuraciones RL
        resultado["configuraciones_rl"] = db.query(ConfiguracionRLDB).filter(
            ConfiguracionRLDB.estado_discretizado.like(f"%{usuario_id}%")
        ).delete(synchronize_session=False)
        
        # 8. Registro de test
        resultado["registro_test"] = db.query(UsuarioTestDB).filter(
            UsuarioTestDB.usuario_id == usuario_id
        ).delete(synchronize_session=False)
        
        # 9. Usuario (al final)
        resultado["usuario"] = db.query(UsuarioDB).filter(
            UsuarioDB.id == usuario_id
        ).delete(synchronize_session=False)
        
        db.commit()
        
        total = sum(resultado.values()) - resultado["usuario_id"]
        logger.info(f"✓ Usuario test {usuario_id} eliminado completamente: {total} registros borrados")
        
        return resultado
        
    except ValueError as ve:
        logger.warning(str(ve))
        raise
    except Exception as e:
        logger.error(f"Error eliminando usuario test: {e}")
        db.rollback()
        raise


def eliminar_todos_usuarios_test(db: Session, tipo_test: Optional[str] = None) -> Dict:
    """
    Elimina TODOS los usuarios de test y sus datos.
    Útil para limpiar después de una sesión de testing.
    
    Args:
        db: Sesión de base de datos
        tipo_test: Si se especifica, solo elimina usuarios de ese tipo (postman, automatico, etc.)
        
    Returns:
        Diccionario con resumen de eliminación
    """
    try:
        # Obtener todos los usuarios de test
        query = db.query(UsuarioTestDB)
        if tipo_test:
            query = query.filter(UsuarioTestDB.tipo_test == tipo_test)
        
        usuarios_test = query.all()
        
        if not usuarios_test:
            return {
                "mensaje": "No hay usuarios de test para eliminar",
                "usuarios_eliminados": 0,
                "total_registros": 0
            }
        
        total_registros = 0
        usuarios_eliminados = []
        
        for usuario_test in usuarios_test:
            resultado = eliminar_usuario_test(db, usuario_test.usuario_id)
            usuarios_eliminados.append({
                "usuario_id": usuario_test.usuario_id,
                "tipo": usuario_test.tipo_test,
                "registros_borrados": sum(resultado.values()) - resultado["usuario_id"]
            })
            total_registros += sum(resultado.values()) - resultado["usuario_id"]
        
        logger.info(f"✓ Limpieza completa: {len(usuarios_eliminados)} usuarios test eliminados, {total_registros} registros totales")
        
        return {
            "mensaje": "Todos los usuarios de test eliminados",
            "usuarios_eliminados": len(usuarios_eliminados),
            "total_registros": total_registros,
            "detalle": usuarios_eliminados
        }
        
    except Exception as e:
        logger.error(f"Error eliminando usuarios test: {e}")
        db.rollback()
        raise


def listar_usuarios_test(db: Session) -> List[Dict]:
    """
    Lista todos los usuarios marcados como test.
    
    Returns:
        Lista de usuarios de test con sus datos
    """
    try:
        usuarios_test = db.query(UsuarioTestDB).join(
            UsuarioDB, UsuarioTestDB.usuario_id == UsuarioDB.id
        ).all()
        
        resultado = []
        for ut in usuarios_test:
            # Contar registros asociados
            counts = {
                "moodmaps": db.query(MoodMapDB).filter(MoodMapDB.usuario_id == ut.usuario_id).count(),
                "feedbacks": db.query(FeedbackDB).filter(FeedbackDB.usuario_id == ut.usuario_id).count(),
                "interacciones": db.query(HistoricoInteraccionDB).filter(HistoricoInteraccionDB.usuario_id == ut.usuario_id).count(),
                "emociones": db.query(EmocionLiberadaDB).filter(EmocionLiberadaDB.usuario_id == ut.usuario_id).count(),
                "gratitudes": db.query(GratitudDB).filter(GratitudDB.usuario_id == ut.usuario_id).count(),
                "destellos": db.query(DestelloDB).filter(DestelloDB.usuario_id == ut.usuario_id).count()
            }
            
            resultado.append({
                "usuario_id": ut.usuario_id,
                "nombre": ut.usuario.nombre,
                "tipo_test": ut.tipo_test,
                "fecha_creacion": ut.fecha_creacion.isoformat(),
                "descripcion": ut.descripcion,
                "registros_asociados": counts,
                "total_registros": sum(counts.values())
            })
        
        return resultado
        
    except Exception as e:
        logger.error(f"Error listando usuarios test: {e}")
        raise


def verificar_es_usuario_test(db: Session, usuario_id: int) -> bool:
    """
    Verifica si un usuario está marcado como test.
    
    Returns:
        True si es usuario de test, False si no
    """
    try:
        existe = db.query(UsuarioTestDB).filter(
            UsuarioTestDB.usuario_id == usuario_id
        ).first()
        
        return existe is not None
        
    except Exception as e:
        logger.error(f"Error verificando usuario test: {e}")
        return False
