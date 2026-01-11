"""
Servicio de Inteligencia Artificial
Incluye RandomForest, Red Neuronal, Clustering y Embeddings
"""

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
from tensorflow import keras
from typing import Dict, List, Tuple
import pickle
import os

from models.usuario import MoodMap, Feedback


class IAService:
    """
    Servicio de IA que maneja:
    - Clasificación con RandomForest
    - Red neuronal ligera para embeddings latentes
    - Clustering de patrones emocionales
    """
    
    def __init__(self):
        """Inicializa los modelos de IA"""
        self.random_forest = None
        self.red_neuronal = None
        self.kmeans = None
        self.scaler = StandardScaler()
        
        # Cargar o entrenar modelos
        self._inicializar_modelos()
    
    def _inicializar_modelos(self):
        """Inicializa o carga los modelos preentrenados"""
        
        # Random Forest para clasificación de estado emocional
        self.random_forest = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        
        # Entrenar con datos sintéticos iniciales
        self._entrenar_random_forest_inicial()
        
        # Red neuronal ligera para embeddings latentes
        self.red_neuronal = self._construir_red_neuronal()
        
        # KMeans para clustering de patrones emocionales
        self.kmeans = KMeans(
            n_clusters=5,  # 5 patrones emocionales principales
            random_state=42
        )
    
    def _construir_red_neuronal(self) -> keras.Model:
        """
        Construye una red neuronal ligera para generar embeddings latentes
        
        Returns:
            Modelo de Keras compilado
        """
        modelo = keras.Sequential([
            # Capa de entrada: 3 valores (felicidad, estrés, motivación)
            keras.layers.Dense(16, activation='relu', input_shape=(3,)),
            keras.layers.Dropout(0.2),
            
            # Capa oculta
            keras.layers.Dense(8, activation='relu'),
            
            # Capa de embedding latente (dimensión reducida)
            keras.layers.Dense(4, activation='relu', name='embedding'),
            
            # Capa de salida: reconstrucción
            keras.layers.Dense(8, activation='relu'),
            keras.layers.Dense(3, activation='sigmoid')
        ])
        
        modelo.compile(
            optimizer='adam',
            loss='mse',
            metrics=['mae']
        )
        
        return modelo
    
    def _entrenar_random_forest_inicial(self):
        """Entrena el Random Forest con datos sintéticos iniciales"""
        # Generar datos sintéticos de entrenamiento
        np.random.seed(42)
        n_samples = 1000
        
        # Características: felicidad, estrés, motivación
        X = np.random.rand(n_samples, 3)
        
        # Etiquetas: estado emocional (0-4)
        # 0: muy bajo, 1: bajo, 2: medio, 3: alto, 4: muy alto
        y = np.zeros(n_samples)
        
        for i in range(n_samples):
            felicidad, estres, motivacion = X[i]
            # Clasificación basada en promedio ponderado
            score = (felicidad * 0.4 + (1 - estres) * 0.3 + motivacion * 0.3)
            
            if score >= 0.8:
                y[i] = 4  # muy alto
            elif score >= 0.6:
                y[i] = 3  # alto
            elif score >= 0.4:
                y[i] = 2  # medio
            elif score >= 0.2:
                y[i] = 1  # bajo
            else:
                y[i] = 0  # muy bajo
        
        self.random_forest.fit(X, y)
    
    def obtener_embedding_emocional(self, moodmap: MoodMap) -> np.ndarray:
        """
        Genera embedding latente del estado emocional usando la red neuronal
        
        Args:
            moodmap: Estado emocional del usuario
            
        Returns:
            Vector de embedding latente
        """
        # Preparar datos de entrada
        X = np.array([[moodmap.felicidad, moodmap.estres, moodmap.motivacion]])
        
        # Obtener embedding de la capa intermedia
        embedding_layer = self.red_neuronal.get_layer('embedding')
        embedding_model = keras.Model(
            inputs=self.red_neuronal.input,
            outputs=embedding_layer.output
        )
        
        embedding = embedding_model.predict(X, verbose=0)
        return embedding[0]
    
    def clasificar_estado(self, moodmap: MoodMap) -> Dict:
        """
        Clasifica el estado emocional usando Random Forest
        
        Args:
            moodmap: Estado emocional del usuario
            
        Returns:
            Diccionario con clasificación y confianza
        """
        X = np.array([[moodmap.felicidad, moodmap.estres, moodmap.motivacion]])
        
        # Predicción
        prediccion = self.random_forest.predict(X)[0]
        probabilidades = self.random_forest.predict_proba(X)[0]
        
        # Mapear predicción a texto
        estados = ["muy bajo", "bajo", "medio", "alto", "muy alto"]
        estado = estados[int(prediccion)]
        
        return {
            "estado": estado,
            "confianza": float(max(probabilidades)),
            "probabilidades": probabilidades.tolist()
        }
    
    def actualizar_clustering(self, embeddings: np.ndarray, feedback: Feedback):
        """
        Actualiza el clustering de patrones emocionales
        
        Args:
            embeddings: Embeddings del estado emocional
            feedback: Feedback del usuario
        """
        # Aquí se actualizaría el modelo de clustering con nuevos datos
        # Por ahora es un placeholder
        pass
    
    def obtener_cluster(self, moodmap: MoodMap) -> int:
        """
        Obtiene el cluster al que pertenece el estado emocional
        
        Args:
            moodmap: Estado emocional del usuario
            
        Returns:
            ID del cluster
        """
        embedding = self.obtener_embedding_emocional(moodmap)
        embedding_reshaped = embedding.reshape(1, -1)
        
        # Predecir cluster
        cluster_id = self.kmeans.predict(embedding_reshaped)[0]
        return int(cluster_id)
    
    def entrenar_con_feedback(self, feedbacks: List[Feedback]):
        """
        Entrena los modelos con feedback acumulado de usuarios
        
        Args:
            feedbacks: Lista de feedbacks de usuarios
        """
        if not feedbacks:
            return
        
        # Preparar datos de entrenamiento
        X = []
        y_efectividad = []
        
        for fb in feedbacks:
            X.append([
                fb.moodmap_previo.felicidad,
                fb.moodmap_previo.estres,
                fb.moodmap_previo.motivacion
            ])
            y_efectividad.append(fb.efectividad)
        
        X = np.array(X)
        y_efectividad = np.array(y_efectividad)
        
        # Reentrenar red neuronal
        self.red_neuronal.fit(
            X, X,  # Autoencoder
            epochs=10,
            batch_size=32,
            verbose=0
        )
        
        print(f"✓ Modelos reentrenados con {len(feedbacks)} feedbacks")
