"""
Servicio de Reinforcement Learning (RL)
Política adaptativa para seleccionar microacciones óptimas
"""

import numpy as np
from typing import Dict, List
from collections import defaultdict
import random

from models.usuario import MoodMap


class RLService:
    """
    Servicio de Reinforcement Learning usando Q-Learning simplificado
    Aprende qué microacciones son más efectivas según el estado emocional
    """
    
    def __init__(self):
        """Inicializa el agente de RL"""
        # Microacciones disponibles
        self.acciones = ["calmarse", "animarse", "activarse"]
        
        # Q-Table: almacena valores Q(estado, acción)
        # Estado se discretiza en rangos: bajo, medio, alto
        self.q_table = defaultdict(lambda: {accion: 0.0 for accion in self.acciones})
        
        # Hiperparámetros
        self.alpha = 0.1  # Tasa de aprendizaje
        self.gamma = 0.9  # Factor de descuento
        self.epsilon = 0.2  # Exploración vs explotación
        
        # Historial de recompensas por acción
        self.historial_recompensas = defaultdict(list)
    
    def _discretizar_estado(self, moodmap: MoodMap) -> str:
        """
        Discretiza el estado emocional continuo en categorías
        
        Args:
            moodmap: Estado emocional del usuario
            
        Returns:
            String que representa el estado discretizado
        """
        def categorizar(valor: float) -> str:
            if valor < 0.33:
                return "bajo"
            elif valor < 0.67:
                return "medio"
            else:
                return "alto"
        
        felicidad_cat = categorizar(moodmap.felicidad)
        estres_cat = categorizar(moodmap.estres)
        motivacion_cat = categorizar(moodmap.motivacion)
        
        return f"{felicidad_cat}_{estres_cat}_{motivacion_cat}"
    
    def seleccionar_microaccion(self, moodmap: MoodMap) -> str:
        """
        Selecciona la mejor microacción usando política ε-greedy
        
        Args:
            moodmap: Estado emocional actual del usuario
            
        Returns:
            Nombre de la microacción seleccionada
        """
        estado = self._discretizar_estado(moodmap)
        
        # Exploración: selección aleatoria
        if random.random() < self.epsilon:
            return random.choice(self.acciones)
        
        # Explotación: seleccionar la mejor acción según Q-values
        q_values = self.q_table[estado]
        mejor_accion = max(q_values, key=q_values.get)
        
        return mejor_accion
    
    def actualizar_politica(
        self,
        microaccion: str,
        recompensa: float,
        estado_previo: MoodMap,
        estado_nuevo: MoodMap = None
    ):
        """
        Actualiza la política de RL con la recompensa recibida
        
        Args:
            microaccion: Acción ejecutada
            recompensa: Recompensa recibida (1-5)
            estado_previo: Estado emocional antes de la acción
            estado_nuevo: Estado emocional después de la acción
        """
        estado_str = self._discretizar_estado(estado_previo)
        
        # Normalizar recompensa a escala 0-1
        recompensa_norm = (recompensa - 1) / 4.0
        
        # Obtener Q-value actual
        q_actual = self.q_table[estado_str][microaccion]
        
        # Calcular nuevo Q-value
        if estado_nuevo:
            estado_nuevo_str = self._discretizar_estado(estado_nuevo)
            max_q_futuro = max(self.q_table[estado_nuevo_str].values())
        else:
            max_q_futuro = 0
        
        # Actualización Q-Learning
        q_nuevo = q_actual + self.alpha * (
            recompensa_norm + self.gamma * max_q_futuro - q_actual
        )
        
        self.q_table[estado_str][microaccion] = q_nuevo
        
        # Guardar en historial
        self.historial_recompensas[microaccion].append(recompensa)
        
        print(f"✓ RL actualizado: {microaccion} en estado {estado_str}")
        print(f"  Q-value: {q_actual:.3f} → {q_nuevo:.3f}")
    
    def obtener_microaccion_adaptativa(self, moodmap: MoodMap) -> Dict:
        """
        Obtiene microacción con análisis detallado
        
        Args:
            moodmap: Estado emocional del usuario
            
        Returns:
            Diccionario con microacción y justificación
        """
        estado = self._discretizar_estado(moodmap)
        microaccion = self.seleccionar_microaccion(moodmap)
        
        # Determinar tipo de respuesta según urgencia
        nivel_urgencia = self._calcular_urgencia(moodmap)
        tipo_respuesta = "larga" if nivel_urgencia == "alta" else "corta"
        
        # Obtener promedio de efectividad de esta acción
        if microaccion in self.historial_recompensas and self.historial_recompensas[microaccion]:
            efectividad_promedio = np.mean(self.historial_recompensas[microaccion])
        else:
            efectividad_promedio = 3.0  # Neutral por defecto
        
        return {
            "microaccion": microaccion,
            "estado_discretizado": estado,
            "tipo_respuesta": tipo_respuesta,
            "nivel_urgencia": nivel_urgencia,
            "efectividad_promedio": float(efectividad_promedio),
            "q_values": dict(self.q_table[estado])
        }
    
    def _calcular_urgencia(self, moodmap: MoodMap) -> str:
        """
        Calcula el nivel de urgencia según el estado emocional
        
        Args:
            moodmap: Estado emocional del usuario
            
        Returns:
            Nivel de urgencia: "baja", "media", "alta"
        """
        # Urgencia alta si el estrés es alto y felicidad/motivación bajas
        if moodmap.estres > 0.7 and (moodmap.felicidad < 0.3 or moodmap.motivacion < 0.3):
            return "alta"
        
        # Urgencia media si hay desequilibrio moderado
        elif moodmap.estres > 0.5 or (moodmap.felicidad < 0.4 and moodmap.motivacion < 0.4):
            return "media"
        
        # Urgencia baja en otros casos
        else:
            return "baja"
    
    def obtener_estadisticas(self) -> Dict:
        """
        Obtiene estadísticas del sistema RL
        
        Returns:
            Diccionario con estadísticas de aprendizaje
        """
        estadisticas = {
            "total_estados_aprendidos": len(self.q_table),
            "microacciones": self.acciones,
            "promedios_recompensa": {}
        }
        
        for accion in self.acciones:
            if accion in self.historial_recompensas and self.historial_recompensas[accion]:
                estadisticas["promedios_recompensa"][accion] = {
                    "promedio": float(np.mean(self.historial_recompensas[accion])),
                    "total_ejecuciones": len(self.historial_recompensas[accion])
                }
            else:
                estadisticas["promedios_recompensa"][accion] = {
                    "promedio": 0.0,
                    "total_ejecuciones": 0
                }
        
        return estadisticas
