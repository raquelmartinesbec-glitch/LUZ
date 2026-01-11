"""
Modelos de base de datos con SQLAlchemy
Definición de tablas que se crearán automáticamente
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class UsuarioDB(Base):
    """Tabla de usuarios del sistema"""
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    avatar = Column(String(255))
    fecha_creacion = Column(DateTime, default=datetime.now)
    fecha_ultima_actividad = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relaciones
    feedbacks = relationship("FeedbackDB", back_populates="usuario", cascade="all, delete-orphan")
    interacciones = relationship("HistoricoInteraccionDB", back_populates="usuario", cascade="all, delete-orphan")
    moodmaps = relationship("MoodMapDB", back_populates="usuario", cascade="all, delete-orphan")


class MoodMapDB(Base):
    """Tabla de estados emocionales (MoodMap)"""
    __tablename__ = "moodmaps"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    felicidad = Column(Float, nullable=False)
    estres = Column(Float, nullable=False)
    motivacion = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.now, index=True)
    
    # Relación con usuario
    usuario = relationship("UsuarioDB", back_populates="moodmaps")


class FeedbackDB(Base):
    """Tabla de feedback de microacciones"""
    __tablename__ = "feedbacks"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    microaccion = Column(String(50), nullable=False, index=True)
    
    # Evaluaciones (1-5)
    efectividad = Column(Float, nullable=False)
    comodidad = Column(Float, nullable=False)
    energia = Column(Float, nullable=False)
    
    # Comentario opcional
    comentario_texto = Column(Text, nullable=True)
    
    # Estados emocionales (JSON)
    moodmap_previo = Column(JSON, nullable=False)
    moodmap_posterior = Column(JSON, nullable=True)
    
    # Metadata
    timestamp = Column(DateTime, default=datetime.now, index=True)
    
    # Relación con usuario
    usuario = relationship("UsuarioDB", back_populates="feedbacks")


class HistoricoInteraccionDB(Base):
    """Tabla de histórico de interacciones del usuario"""
    __tablename__ = "historico_interacciones"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    
    # Tipo de interacción
    tipo = Column(String(50), nullable=False, index=True)  # moodmap, alma_board, microaccion
    
    # Datos de la interacción (JSON flexible)
    datos = Column(JSON, nullable=False)
    
    # Resultado de IA
    embedding_latente = Column(JSON, nullable=True)
    cluster_id = Column(Integer, nullable=True)
    microaccion_sugerida = Column(String(50), nullable=True)
    
    # Metadata
    fecha = Column(DateTime, default=datetime.now, index=True)
    
    # Relación con usuario
    usuario = relationship("UsuarioDB", back_populates="interacciones")


class EmocionLiberadaDB(Base):
    """Tabla de emociones tóxicas liberadas en Alma Board"""
    __tablename__ = "emociones_liberadas"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    emocion = Column(String(100), nullable=False)
    categoria = Column(String(50))  # toxica, constructiva, neutral
    intensidad_estimada = Column(Float)
    fecha_liberacion = Column(DateTime, default=datetime.now, index=True)


class GratitudDB(Base):
    """Tabla de microacciones de gratitud"""
    __tablename__ = "gratitudes"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    texto_gratitud = Column(Text, nullable=False)
    tipo = Column(String(50))  # escrito, dibujado, meditacion, etc.
    embedding_texto = Column(JSON, nullable=True)
    fecha_creacion = Column(DateTime, default=datetime.now, index=True)


class DestelloDB(Base):
    """Tabla de destellos de luz generados"""
    __tablename__ = "destellos"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    color = Column(String(50), nullable=False)
    forma = Column(String(50), nullable=False)
    tamano = Column(Float, default=1.0)
    intensidad = Column(Float, default=1.0)
    accion_origen = Column(String(100))  # Qué acción generó el destello
    fecha_creacion = Column(DateTime, default=datetime.now, index=True)


class ConfiguracionRLDB(Base):
    """Tabla para almacenar la Q-Table del Reinforcement Learning"""
    __tablename__ = "configuracion_rl"
    
    id = Column(Integer, primary_key=True, index=True)
    estado_discretizado = Column(String(100), nullable=False, unique=True, index=True)
    q_values = Column(JSON, nullable=False)  # {accion: q_value}
    ultima_actualizacion = Column(DateTime, default=datetime.now, onupdate=datetime.now)


# ==========================================
# TABLA DE USUARIOS DE TEST (POSTMAN)
# ==========================================
# Usuarios creados para tests que se pueden eliminar sin dejar rastro

class UsuarioTestDB(Base):
    """
    Tabla para marcar usuarios creados para testing (Postman, etc.)
    Permite eliminar completamente todos los datos de un usuario de test.
    """
    __tablename__ = "usuarios_test"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), unique=True, nullable=False)
    tipo_test = Column(String(50), default="postman")  # postman, automatico, manual
    fecha_creacion = Column(DateTime, default=datetime.now, index=True)
    descripcion = Column(String(255), nullable=True)
    
    # Relación con Usuario
    usuario = relationship("UsuarioDB", foreign_keys=[usuario_id])


# ==========================================
# TABLAS DE ARCHIVO HISTÓRICO PARA INVESTIGACIÓN
# ==========================================
# Estas tablas NUNCA se borran automáticamente.
# Contienen datos consolidados y limpios para análisis futuros e investigación.

class ArchivoEmocionalDB(Base):
    """
    Archivo permanente de datos emocionales consolidados.
    Se usa para investigación y análisis longitudinal.
    NUNCA se borra automáticamente - Los datos se preservan indefinidamente.
    """
    __tablename__ = "archivo_emocional"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, nullable=True)  # Puede ser NULL si se elimina el usuario
    # Datos del MoodMap original
    felicidad = Column(Float, nullable=False)
    estres = Column(Float, nullable=False)
    motivacion = Column(Float, nullable=False)
    # Embedding latente del estado emocional
    embedding_latente = Column(JSON, nullable=True)
    # Clasificación del cluster
    cluster_id = Column(Integer, nullable=True)
    # Microacción recomendada
    microaccion_recomendada = Column(String(50), nullable=True)
    # Feedback del usuario (si lo dio)
    feedback_efectividad = Column(Float, nullable=True)  # 1-5
    feedback_comodidad = Column(Float, nullable=True)    # 1-5
    feedback_energia = Column(Float, nullable=True)      # 1-5
    # Metadata
    fecha_registro = Column(DateTime, nullable=False, index=True)
    fecha_archivo = Column(DateTime, default=datetime.now)  # Cuándo se archivó
    semana_anio = Column(String(10), nullable=True, index=True)  # "2026-W02" para agrupación
    # Datos adicionales en JSON (flexibilidad para futuras extensiones)
    datos_extra = Column(JSON, nullable=True)


class ArchivoAlmaBoardDB(Base):
    """
    Archivo permanente de datos del Alma Board.
    Emociones liberadas y gratitudes consolidadas.
    NUNCA se borra automáticamente - Datos valiosos para investigación.
    """
    __tablename__ = "archivo_alma_board"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, nullable=True)  # Puede ser NULL
    tipo = Column(String(20), nullable=False, index=True)  # "emocion" o "gratitud"
    # Para emociones
    emocion = Column(String(100), nullable=True)
    categoria = Column(String(50), nullable=True)  # toxica, constructiva, neutral
    intensidad = Column(Float, nullable=True)
    # Para gratitudes
    texto = Column(Text, nullable=True)
    embedding_texto = Column(JSON, nullable=True)  # Vector semántico
    # Metadata
    fecha_registro = Column(DateTime, nullable=False, index=True)
    fecha_archivo = Column(DateTime, default=datetime.now)
    semana_anio = Column(String(10), nullable=True, index=True)
    mes_anio = Column(String(10), nullable=True, index=True)  # "2026-01"
    # Datos adicionales
    datos_extra = Column(JSON, nullable=True)


class ResumenSemanalDB(Base):
    """
    Resumen consolidado semanal de datos del usuario.
    Agregaciones estadísticas listas para análisis e investigación.
    NUNCA se borra automáticamente.
    """
    __tablename__ = "resumen_semanal"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, nullable=True)
    semana_anio = Column(String(10), nullable=False, index=True)  # "2026-W02"
    anio = Column(Integer, nullable=False)
    semana = Column(Integer, nullable=False)
    
    # Estadísticas emocionales
    num_registros = Column(Integer, default=0)
    felicidad_promedio = Column(Float, nullable=True)
    estres_promedio = Column(Float, nullable=True)
    motivacion_promedio = Column(Float, nullable=True)
    felicidad_max = Column(Float, nullable=True)
    estres_max = Column(Float, nullable=True)
    motivacion_max = Column(Float, nullable=True)
    
    # Microacciones
    num_microacciones = Column(Integer, default=0)
    microacciones_mas_usadas = Column(JSON, nullable=True)  # Top 5
    efectividad_promedio = Column(Float, nullable=True)
    
    # Alma Board
    num_emociones_liberadas = Column(Integer, default=0)
    num_gratitudes = Column(Integer, default=0)
    emociones_mas_frecuentes = Column(JSON, nullable=True)
    
    # Metadata
    fecha_creacion = Column(DateTime, default=datetime.now)
    fecha_actualizacion = Column(DateTime, default=datetime.now, onupdate=datetime.now)
