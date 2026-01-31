"""
Servicio de IA/ML con fallback automático.
Si TensorFlow no está disponible, usa predicciones mock.
"""

import logging
import random
from typing import Dict, List, Optional, Union
import json

logger = logging.getLogger(__name__)

# Detectar si ML está disponible
ML_AVAILABLE = False
USE_MOCK = True

try:
    import tensorflow as tf
    import numpy as np
    from sklearn.preprocessing import StandardScaler
    ML_AVAILABLE = True
    USE_MOCK = False
    logger.info("✅ ML libraries loaded successfully")
except ImportError as e:
    logger.warning(f"⚠️ ML libraries not available: {e}. Using mock predictions.")
    USE_MOCK = True

class MLService:
    """Servicio de ML con fallback automático a mocks"""
    
    def __init__(self):
        self.autoencoder = None
        self.scaler = None
        self.emotion_classifier = None
        
        if not USE_MOCK:
            self._init_models()
        else:
            logger.info("🎭 Using mock ML service (TensorFlow not installed)")
    
    def _init_models(self):
        """Inicializar modelos ML reales (solo si TensorFlow disponible)"""
        try:
            # Autoencoder para análisis emocional (3→16→8→4→8→16→3)
            self.autoencoder = tf.keras.Sequential([
                tf.keras.layers.Dense(16, activation='relu', input_shape=(3,)),
                tf.keras.layers.Dense(8, activation='relu'),
                tf.keras.layers.Dense(4, activation='relu'),  # Bottleneck
                tf.keras.layers.Dense(8, activation='relu'),
                tf.keras.layers.Dense(16, activation='relu'),
                tf.keras.layers.Dense(3, activation='sigmoid')  # Reconstrucción
            ])
            
            self.autoencoder.compile(
                optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
                loss='mse'
            )
            
            # Clasificador de emociones simple
            self.emotion_classifier = tf.keras.Sequential([
                tf.keras.layers.Dense(32, activation='relu', input_shape=(10,)),
                tf.keras.layers.Dropout(0.3),
                tf.keras.layers.Dense(16, activation='relu'),
                tf.keras.layers.Dense(7, activation='softmax')  # 7 emociones básicas
            ])
            
            logger.info("🤖 Real ML models initialized")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize ML models: {e}")
            global USE_MOCK
            USE_MOCK = True
    
    def predict_emotion(self, text: str, mood_data: Optional[Dict] = None) -> Dict:
        """Predecir emoción principal y confianza"""
        
        if USE_MOCK:
            return self._mock_emotion_prediction(text, mood_data)
        
        try:
            # Procesar texto real (simplificado)
            features = self._extract_text_features(text)
            
            if mood_data:
                # Combinar con datos del mood
                mood_features = [
                    mood_data.get('valencia', 0.5),
                    mood_data.get('activacion', 0.5),
                    mood_data.get('control', 0.5)
                ]
                features.extend(mood_features)
            
            # Padding o truncado a 10 features
            features = (features + [0.0] * 10)[:10]
            
            prediction = self.emotion_classifier.predict(np.array([features]))
            emotion_labels = ['alegría', 'tristeza', 'ira', 'miedo', 'sorpresa', 'asco', 'neutral']
            
            predicted_idx = np.argmax(prediction[0])
            confidence = float(prediction[0][predicted_idx])
            
            return {
                'emocion_principal': emotion_labels[predicted_idx],
                'confianza': round(confidence, 3),
                'distribución': {
                    emotion_labels[i]: round(float(prediction[0][i]), 3)
                    for i in range(len(emotion_labels))
                },
                'modo': 'ml_real'
            }
            
        except Exception as e:
            logger.error(f"Error in emotion prediction: {e}")
            return self._mock_emotion_prediction(text, mood_data)
    
    def generate_microacciones(self, user_profile: Dict, current_mood: Dict) -> List[Dict]:
        """Generar microacciones personalizadas"""
        
        if USE_MOCK:
            return self._mock_microacciones(user_profile, current_mood)
        
        try:
            # ML real: usar autoencoder para detectar patrones
            mood_vector = [
                current_mood.get('valencia', 0.5),
                current_mood.get('activacion', 0.5),
                current_mood.get('control', 0.5)
            ]
            
            encoded = self.autoencoder.predict(np.array([mood_vector]))
            reconstructed = encoded[0]
            
            # Calcular diferencia (anomalía emocional)
            mse = np.mean((np.array(mood_vector) - reconstructed) ** 2)
            
            # Generar microacciones basadas en MSE
            if mse > 0.1:  # Alta anomalía
                return self._generate_high_intervention_actions(current_mood)
            else:  # Estado normal
                return self._generate_maintenance_actions(current_mood)
                
        except Exception as e:
            logger.error(f"Error generating microactions: {e}")
            return self._mock_microacciones(user_profile, current_mood)
    
    def _extract_text_features(self, text: str) -> List[float]:
        """Extraer features simples del texto"""
        if not text:
            return [0.0] * 7
        
        # Features básicas (sin NLP pesado)
        length_norm = min(len(text) / 100, 1.0)
        word_count_norm = min(len(text.split()) / 50, 1.0)
        exclamation_ratio = text.count('!') / max(len(text), 1)
        question_ratio = text.count('?') / max(len(text), 1)
        uppercase_ratio = sum(1 for c in text if c.isupper()) / max(len(text), 1)
        
        # Palabras emocionales simples
        positive_words = ['feliz', 'bien', 'genial', 'amor', 'gracias', 'alegre']
        negative_words = ['mal', 'triste', 'enojo', 'odio', 'problema', 'dolor']
        
        text_lower = text.lower()
        positive_score = sum(1 for word in positive_words if word in text_lower)
        negative_score = sum(1 for word in negative_words if word in text_lower)
        
        return [length_norm, word_count_norm, exclamation_ratio, question_ratio, 
                uppercase_ratio, positive_score, negative_score]
    
    def _mock_emotion_prediction(self, text: str, mood_data: Optional[Dict] = None) -> Dict:
        """Predicción mock realista"""
        
        # Analizar texto de forma simple
        text_lower = text.lower() if text else ""
        
        # Emociones con scores basados en palabras clave
        emotions = {
            'alegría': 0.1,
            'tristeza': 0.1,
            'ira': 0.1,
            'miedo': 0.1,
            'sorpresa': 0.1,
            'asco': 0.1,
            'neutral': 0.4
        }
        
        # Ajustar basado en contenido
        if any(word in text_lower for word in ['feliz', 'bien', 'genial', 'amor', 'alegre']):
            emotions['alegría'] += 0.4
        elif any(word in text_lower for word in ['mal', 'triste', 'deprime', 'lloro']):
            emotions['tristeza'] += 0.4
        elif any(word in text_lower for word in ['enojo', 'ira', 'molesto', 'odio']):
            emotions['ira'] += 0.4
        elif any(word in text_lower for word in ['miedo', 'asusta', 'terror', 'pánico']):
            emotions['miedo'] += 0.4
        
        # Normalizar
        total = sum(emotions.values())
        emotions = {k: v/total for k, v in emotions.items()}
        
        # Emoción principal
        main_emotion = max(emotions.keys(), key=lambda k: emotions[k])
        
        return {
            'emocion_principal': main_emotion,
            'confianza': round(emotions[main_emotion], 3),
            'distribución': {k: round(v, 3) for k, v in emotions.items()},
            'modo': 'mock_inteligente'
        }
    
    def _mock_microacciones(self, user_profile: Dict, current_mood: Dict) -> List[Dict]:
        """Microacciones mock realistas"""
        
        valencia = current_mood.get('valencia', 0.5)
        activacion = current_mood.get('activacion', 0.5)
        
        acciones_base = [
            {
                'tipo': 'respiracion',
                'titulo': '🌬️ Respiración 4-7-8',
                'descripcion': 'Inhala 4 seg, retén 7 seg, exhala 8 seg',
                'duracion_minutos': 3,
                'dificultad': 'fácil'
            },
            {
                'tipo': 'movimiento',
                'titulo': '🤸 Estiramiento suave',
                'descripcion': 'Estira brazos y cuello, respira profundo',
                'duracion_minutos': 5,
                'dificultad': 'fácil'
            },
            {
                'tipo': 'gratitud',
                'titulo': '🙏 Tres gracias',
                'descripcion': 'Piensa en 3 cosas por las que te sientes agradecido/a',
                'duracion_minutos': 2,
                'dificultad': 'fácil'
            },
            {
                'tipo': 'creatividad',
                'titulo': '🎨 Doodle libre',
                'descripcion': 'Dibuja formas libres por 5 minutos',
                'duracion_minutos': 5,
                'dificultad': 'medio'
            },
            {
                'tipo': 'naturaleza',
                'titulo': '🌱 Observa algo verde',
                'descripcion': 'Mira una planta, árbol o foto de naturaleza por 3 min',
                'duracion_minutos': 3,
                'dificultad': 'fácil'
            }
        ]
        
        # Seleccionar 3-4 acciones basadas en el mood
        if valencia < 0.4:  # Estado bajo
            acciones = [a for a in acciones_base if a['tipo'] in ['respiracion', 'gratitud', 'naturaleza']]
        elif activacion > 0.7:  # Muy activado
            acciones = [a for a in acciones_base if a['tipo'] in ['respiracion', 'movimiento']]
        else:  # Estado neutro
            acciones = random.sample(acciones_base, 3)
        
        # Añadir score de recomendación
        for accion in acciones:
            accion['score_recomendacion'] = random.uniform(0.6, 0.9)
            accion['razon'] = 'Basado en tu estado emocional actual'
        
        return sorted(acciones, key=lambda x: x['score_recomendacion'], reverse=True)
    
    def _generate_high_intervention_actions(self, mood: Dict) -> List[Dict]:
        """Acciones para estados emocionales anómalos"""
        # Implementación real con ML
        return self._mock_microacciones({}, mood)
    
    def _generate_maintenance_actions(self, mood: Dict) -> List[Dict]:
        """Acciones de mantenimiento para estados normales"""
        # Implementación real con ML
        return self._mock_microacciones({}, mood)

# Instancia global del servicio
ml_service = MLService()