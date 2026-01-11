"""
Servicio de NLP (Natural Language Processing)
Procesa texto, genera embeddings y frases motivadoras estilo boho chic zen
"""

from sentence_transformers import SentenceTransformer
import numpy as np
from typing import Dict, List
import random

from models.usuario import MoodMap


class NLPService:
    """
    Servicio de NLP que maneja:
    - Embeddings de texto con sentence-transformers
    - Análisis de sentimiento
    - Generación de frases motivadoras estilo boho chic zen
    """
    
    def __init__(self):
        """Inicializa el modelo de embeddings"""
        # Usar modelo ligero de sentence-transformers
        try:
            self.modelo_embeddings = SentenceTransformer('paraphrase-MiniLM-L6-v2')
        except:
            # Fallback si no está disponible
            self.modelo_embeddings = None
            print("⚠ Modelo de embeddings no disponible. Usando embeddings simulados.")
        
        # Frases motivadoras predefinidas estilo boho chic zen
        self._cargar_frases_motivadoras()
    
    def _cargar_frases_motivadoras(self):
        """Carga las frases motivadoras categorizadas por microacción"""
        self.frases = {
            "calmarse": [
                "Respira profundo, cada inhalación trae calma a tu ser 🌊",
                "En este momento de quietud, encuentra tu centro 🕊️",
                "Deja que la paz fluya a través de ti como un río suave ✨",
                "Tu mente merece este espacio de serenidad 🌸",
                "Suelta lo que no puedes controlar, abraza lo que sí 🍃",
            ],
            "animarse": [
                "Tu luz interior brilla más de lo que imaginas ✨",
                "Eres capaz de crear magia en cada día 🌟",
                "Permite que la alegría dance en tu corazón 💫",
                "Cada sonrisa es un regalo que te das a ti mismo 🌺",
                "Tu energía positiva ilumina el mundo a tu alrededor ☀️",
            ],
            "activarse": [
                "Tu cuerpo es un templo lleno de energía vital 💪",
                "Cada movimiento es una celebración de la vida 🌿",
                "Despierta la fuerza que habita en ti 🔥",
                "La acción transforma tus sueños en realidad 🚀",
                "Tu energía crea cambios maravillosos 🌈",
            ],
            "liberacion": [
                "Soltar es un acto de amor propio 🌊",
                "Lo que dejas ir hace espacio para lo nuevo ✨",
                "Cada emoción liberada te hace más ligero 🦋",
                "Honra tus sentimientos y déjalos fluir 🍃",
                "Al liberar, te liberas 🕊️",
            ],
            "gratitud": [
                "La gratitud transforma lo ordinario en extraordinario ✨",
                "Cada momento de agradecimiento eleva tu espíritu 🌟",
                "Cultivar gratitud es sembrar semillas de felicidad 🌱",
                "Tu corazón agradecido atrae más bendiciones 💫",
                "En la gratitud, encuentras la verdadera abundancia 🌺",
            ],
            "general": [
                "Confía en el proceso, todo llega en su momento perfecto ✨",
                "Eres exactamente donde necesitas estar ahora 🌸",
                "Tu viaje de bienestar es único y hermoso 🦋",
                "Cada pequeño paso te acerca a tu mejor versión 🌟",
                "Honra tu ritmo, respeta tu proceso 🍃",
            ]
        }
    
    def obtener_embeddings_texto(self, texto: str) -> np.ndarray:
        """
        Genera embeddings del texto usando sentence-transformers
        
        Args:
            texto: Texto a procesar
            
        Returns:
            Vector de embeddings
        """
        if not texto:
            return np.zeros(384)  # Dimensión del modelo MiniLM
        
        if self.modelo_embeddings:
            embeddings = self.modelo_embeddings.encode(texto)
            return embeddings
        else:
            # Embeddings simulados si el modelo no está disponible
            # En producción, esto debería reemplazarse con el modelo real
            np.random.seed(hash(texto) % 2**32)
            return np.random.rand(384)
    
    def analizar_sentimiento(self, texto: str) -> Dict:
        """
        Analiza el sentimiento del texto
        
        Args:
            texto: Texto a analizar
            
        Returns:
            Diccionario con análisis de sentimiento
        """
        if not texto:
            return {"sentimiento": "neutral", "confianza": 0.0}
        
        # Análisis simple basado en palabras clave
        # En producción, usar un modelo más sofisticado
        
        palabras_positivas = [
            "bien", "mejor", "feliz", "alegre", "contento", "genial",
            "excelente", "maravilloso", "perfecto", "gracias", "amor"
        ]
        
        palabras_negativas = [
            "mal", "peor", "triste", "difícil", "duro", "no pude",
            "frustrado", "cansado", "estresado", "preocupado"
        ]
        
        texto_lower = texto.lower()
        
        puntos_positivos = sum(1 for palabra in palabras_positivas if palabra in texto_lower)
        puntos_negativos = sum(1 for palabra in palabras_negativas if palabra in texto_lower)
        
        total_puntos = puntos_positivos + puntos_negativos
        
        if total_puntos == 0:
            return {"sentimiento": "neutral", "confianza": 0.5}
        
        if puntos_positivos > puntos_negativos:
            return {
                "sentimiento": "positivo",
                "confianza": min(puntos_positivos / (total_puntos + 1), 1.0)
            }
        elif puntos_negativos > puntos_positivos:
            return {
                "sentimiento": "negativo",
                "confianza": min(puntos_negativos / (total_puntos + 1), 1.0)
            }
        else:
            return {"sentimiento": "neutral", "confianza": 0.5}
    
    def generar_frase_motivadora(self, moodmap: MoodMap, microaccion: str) -> str:
        """
        Genera una frase motivadora según el contexto
        
        Args:
            moodmap: Estado emocional del usuario
            microaccion: Microacción sugerida
            
        Returns:
            Frase motivadora personalizada
        """
        categoria = microaccion if microaccion in self.frases else "general"
        frases_disponibles = self.frases[categoria]
        
        # Seleccionar frase aleatoria de la categoría
        frase = random.choice(frases_disponibles)
        
        return frase
    
    def generar_frase_liberacion(self, emocion: str) -> str:
        """
        Genera una frase de apoyo para la liberación de emociones
        
        Args:
            emocion: Emoción que se está liberando
            
        Returns:
            Frase de apoyo
        """
        frases_liberacion = [
            f"Reconoces tu {emocion}, la honras y la dejas ir con amor 🌊",
            f"Es valiente soltar la {emocion}. Estás creando espacio para la paz ✨",
            f"Al liberar la {emocion}, te permites florecer 🌸",
            f"Tu {emocion} fue parte de tu camino, ahora puedes seguir adelante 🦋",
            f"Suelta la {emocion}, confía en tu proceso de sanación 🍃",
        ]
        
        return random.choice(frases_liberacion)
    
    def generar_frase_gratitud(self, gratitud: str) -> str:
        """
        Genera una frase motivadora para momentos de gratitud
        
        Args:
            gratitud: Texto de gratitud del usuario
            
        Returns:
            Frase motivadora de respuesta
        """
        frases_respuesta = [
            "Hermoso gesto de gratitud. Tu corazón agradecido atrae más luz ✨",
            "Cada momento de agradecimiento eleva tu espíritu. Sigue brillando 🌟",
            "La gratitud que cultivas transforma tu realidad 💫",
            "Qué hermosa forma de honrar tus bendiciones 🌺",
            "Tu gratitud crea ondas de positividad a tu alrededor 🌈",
        ]
        
        return random.choice(frases_respuesta)
    
    def analizar_emocion(self, emocion: str) -> Dict:
        """
        Analiza una emoción textual
        
        Args:
            emocion: Nombre de la emoción
            
        Returns:
            Análisis de la emoción
        """
        # Categorías de emociones
        emociones_toxicas = [
            "ansiedad", "miedo", "frustración", "preocupación",
            "tristeza", "ira", "culpa", "vergüenza", "envidia"
        ]
        
        emociones_constructivas = [
            "alegría", "gratitud", "amor", "paz", "esperanza",
            "motivación", "entusiasmo", "confianza"
        ]
        
        emocion_lower = emocion.lower()
        
        if any(tox in emocion_lower for tox in emociones_toxicas):
            categoria = "tóxica"
            intensidad_estimada = 0.7
        elif any(const in emocion_lower for const in emociones_constructivas):
            categoria = "constructiva"
            intensidad_estimada = 0.3
        else:
            categoria = "neutral"
            intensidad_estimada = 0.5
        
        return {
            "emocion": emocion,
            "categoria": categoria,
            "intensidad_estimada": intensidad_estimada,
            "recomendacion": self._obtener_recomendacion_emocion(categoria)
        }
    
    def _obtener_recomendacion_emocion(self, categoria: str) -> str:
        """Obtiene una recomendación según la categoría de emoción"""
        recomendaciones = {
            "tóxica": "Es importante reconocer y liberar esta emoción con compasión",
            "constructiva": "Cultiva y expande esta emoción positiva",
            "neutral": "Observa esta emoción sin juicio, simplemente déjala ser"
        }
        
        return recomendaciones.get(categoria, "Honra tus emociones con amor")
