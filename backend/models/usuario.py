"""
Modelos de datos para el backend de Luz
Pydantic models para validación y serialización
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class MoodMap(BaseModel):
    """Modelo del MoodMap con estados emocionales normalizados 0-1"""
    felicidad: float = Field(ge=0.0, le=1.0, description="Nivel de felicidad")
    estres: float = Field(ge=0.0, le=1.0, description="Nivel de estrés")
    motivacion: float = Field(ge=0.0, le=1.0, description="Nivel de motivación")


class Microaccion(BaseModel):
    """Modelo de microacción ejecutada"""
    accion: str = Field(description="Nombre de la microacción")
    feedback: Optional[int] = Field(None, ge=1, le=5, description="Feedback del usuario (1-5)")
    fecha_ejecucion: Optional[datetime] = None


class AlmaBoard(BaseModel):
    """Modelo del Alma Board"""
    emociones_toxicas_liberadas: List[str] = Field(default_factory=list)
    microacciones_gratitud: List[str] = Field(default_factory=list)


class Destello(BaseModel):
    """Modelo de destello de luz personalizable"""
    color: str
    forma: str
    tamano: float = Field(default=1.0, ge=0.5, le=2.0)
    intensidad: float = Field(default=1.0, ge=0.0, le=1.0)


class Usuario(BaseModel):
    """Modelo completo de usuario"""
    id: Optional[int] = None
    nombre: str
    avatar: str
    moodmap: MoodMap
    microacciones: List[Microaccion] = Field(default_factory=list)
    alma_board: AlmaBoard = Field(default_factory=AlmaBoard)
    destellos: List[Destello] = Field(default_factory=list)


class Feedback(BaseModel):
    """Modelo de feedback post-microacción"""
    usuario_id: int
    microaccion: str
    efectividad: float = Field(ge=1.0, le=5.0, description="Efectividad de la microacción")
    comodidad: float = Field(ge=1.0, le=5.0, description="Comodidad durante la ejecución")
    energia: float = Field(ge=1.0, le=5.0, description="Impacto en la energía")
    comentario_texto: Optional[str] = None
    moodmap_previo: MoodMap
    moodmap_posterior: Optional[MoodMap] = None
    timestamp: datetime = Field(default_factory=datetime.now)


class EstadoEmocional(BaseModel):
    """Modelo de estado emocional procesado"""
    clasificacion: str
    confianza: float
    embedding_latente: Optional[List[float]] = None
    cluster_id: Optional[int] = None


class RespuestaIA(BaseModel):
    """Modelo de respuesta del sistema de IA"""
    microaccion_sugerida: str
    tipo_respuesta: str = Field(description="corta o larga")
    frase_motivadora: str
    nivel_urgencia: Optional[str] = None
