"""
Utilidad para cargar y usar los modelos entrenados de LUZ
Este script facilita la carga y uso de los modelos de:
1. Predicción de emociones (Random Forest)
2. Clustering de microacciones (KMeans)
3. Predicción de gratitudes (Random Forest)
4. Análisis de MoodMaps (KMeans + RandomForest)
"""

import pickle
import joblib
import numpy as np
import pandas as pd
import os
from typing import Dict, List, Tuple, Any
from sklearn.preprocessing import StandardScaler

class ModelosLUZ:
    """Clase para manejar todos los modelos entrenados de LUZ"""
    
    def __init__(self, models_dir: str = "modelos_entrenados"):
        self.models_dir = models_dir
        
        # Verificar si el directorio existe
        if not os.path.exists(models_dir):
            print(f"⚠️ Directorio {models_dir} no encontrado. Verificar ruta.")
            return
        
        # Emociones liberadas
        self.modelo_emociones = None
        self.metadata_emociones = None
        
        # Microacciones (clustering)
        self.modelo_clustering_microacciones = None
        self.scaler_clustering = None
        self.metadata_clustering = None
        
        # Gratitudes
        self.modelo_gratitudes = None
        self.metadata_gratitudes = None
        
        # MoodMaps
        self.modelo_clustering_moodmaps = None
        self.scaler_moodmaps = None
        self.modelos_prediccion_moodmaps = None
        self.metadata_moodmaps = None
        
        print("ModelosLUZ inicializado - Listo para cargar modelos")
    
    def listar_modelos_disponibles(self):
        """Listar todos los archivos de modelos disponibles"""
        print("MODELOS DISPONIBLES:")
        print("="*40)
        
        archivos = os.listdir(self.models_dir)
        modelos_encontrados = [f for f in archivos if f.endswith('.pkl')]
        
        if modelos_encontrados:
            for modelo in sorted(modelos_encontrados):
                print(f"   📦 {modelo}")
        else:
            print("   ❌ No se encontraron modelos (.pkl)")
        
        return modelos_encontrados
    
    def cargar_modelo_emociones(self):
        """Cargar modelo de predicción de emociones liberadas"""
        try:
            modelo_file = os.path.join(self.models_dir, "modelo_prediccion_emociones.pkl")
            metadata_file = os.path.join(self.models_dir, "metadata_emociones.pkl")
            
            self.modelo_emociones = joblib.load(modelo_file)
            
            with open(metadata_file, 'rb') as f:
                self.metadata_emociones = pickle.load(f)
            
            print(f"✅ Modelo de emociones cargado exitosamente")
            print(f"   Accuracy: {self.metadata_emociones['accuracy']:.1%}")
            print(f"   Emociones disponibles: {len(self.metadata_emociones['target_names'])}")
            return True
            
        except Exception as e:
            print(f"❌ Error cargando modelo de emociones: {e}")
            return False
    
    def cargar_modelo_microacciones(self):
        """Cargar modelo de clustering de microacciones"""
        try:
            clustering_file = os.path.join(self.models_dir, "modelo_clustering_microacciones.pkl")
            scaler_file = os.path.join(self.models_dir, "scaler_clustering.pkl")
            metadata_file = os.path.join(self.models_dir, "metadata_clustering.pkl")
            
            self.modelo_clustering_microacciones = joblib.load(clustering_file)
            self.scaler_clustering = joblib.load(scaler_file)
            
            with open(metadata_file, 'rb') as f:
                self.metadata_clustering = pickle.load(f)
            
            print(f"✅ Modelo de microacciones cargado exitosamente")
            print(f"   Clusters: {self.metadata_clustering['n_clusters']}")
            print(f"   Features: {len(self.metadata_clustering['feature_names'])}")
            return True
            
        except Exception as e:
            print(f"❌ Error cargando modelo de microacciones: {e}")
            return False
    
    def cargar_modelo_gratitudes(self):
        """Cargar modelo de predicción de gratitudes"""
        try:
            modelo_file = os.path.join(self.models_dir, "modelo_prediccion_gratitudes.pkl")
            metadata_file = os.path.join(self.models_dir, "metadata_gratitudes.pkl")
            
            self.modelo_gratitudes = joblib.load(modelo_file)
            
            with open(metadata_file, 'rb') as f:
                self.metadata_gratitudes = pickle.load(f)
            
            print(f"✅ Modelo de gratitudes cargado exitosamente")
            print(f"   Accuracy: {self.metadata_gratitudes['accuracy']:.1%}")
            print(f"   Gratitudes disponibles: {len(self.metadata_gratitudes['target_names'])}")
            return True
            
        except Exception as e:
            print(f"❌ Error cargando modelo de gratitudes: {e}")
            return False
    
    def cargar_modelo_moodmaps(self):
        """Cargar modelos de MoodMaps (clustering y predicción)"""
        try:
            clustering_file = os.path.join(self.models_dir, "modelo_clustering_moodmaps.pkl")
            scaler_file = os.path.join(self.models_dir, "scaler_moodmaps.pkl")
            modelos_pred_file = os.path.join(self.models_dir, "modelos_prediccion_moodmaps.pkl")
            metadata_file = os.path.join(self.models_dir, "metadata_moodmaps.pkl")
            
            self.modelo_clustering_moodmaps = joblib.load(clustering_file)
            self.scaler_moodmaps = joblib.load(scaler_file)
            self.modelos_prediccion_moodmaps = joblib.load(modelos_pred_file)
            
            with open(metadata_file, 'rb') as f:
                self.metadata_moodmaps = pickle.load(f)
            
            print(f"✅ Modelos de MoodMaps cargados exitosamente")
            print(f"   Accuracy promedio: {self.metadata_moodmaps['accuracy_promedio']:.1%}")
            print(f"   Clusters identificados: {self.metadata_moodmaps['n_clusters']}")
            print(f"   Emociones modeladas: {len(self.metadata_moodmaps['emociones_predichas'])}")
            return True
            
        except Exception as e:
            print(f"❌ Error cargando modelos de MoodMaps: {e}")
            return False
    
    def predecir_emocion(self, usuario_id, dia, hora):
        """Predecir emoción liberada basada en usuario, día y hora"""
        if self.modelo_emociones is None:
            print("⚠️ Modelo de emociones no cargado. Ejecutar cargar_modelo_emociones() primero")
            return None
            
        try:
            # Preparar datos de entrada
            X_pred = np.array([[usuario_id, dia, hora]])
            
            # Hacer predicción
            prediccion = self.modelo_emociones.predict(X_pred)[0]
            probabilidades = self.modelo_emociones.predict_proba(X_pred)[0]
            
            emocion_predicha = self.metadata_emociones['target_names'][prediccion]
            confianza = max(probabilidades) * 100
            
            return {
                'emocion': emocion_predicha,
                'confianza': confianza,
                'usuario_id': usuario_id,
                'dia': dia,
                'hora': hora
            }
            
        except Exception as e:
            print(f"❌ Error en predicción de emoción: {e}")
            return None
    
    def clasificar_microaccion(self, felicidad_z, estres_z, motivacion_z, efectividad, energia):
        """Clasificar patrón de microacción usando clustering"""
        if self.modelo_clustering_microacciones is None or self.scaler_clustering is None:
            print("⚠️ Modelo de microacciones no cargado. Ejecutar cargar_modelo_microacciones() primero")
            return None
            
        try:
            # Preparar datos de entrada
            X_input = np.array([[felicidad_z, estres_z, motivacion_z, efectividad, energia]])
            X_scaled = self.scaler_clustering.transform(X_input)
            
            # Predecir cluster
            cluster = self.modelo_clustering_microacciones.predict(X_scaled)[0]
            distancias = self.modelo_clustering_microacciones.transform(X_scaled)[0]
            
            return {
                'cluster': int(cluster),
                'distancias': distancias.tolist(),
                'perfil_emocional': {
                    'felicidad_z': felicidad_z,
                    'estres_z': estres_z,
                    'motivacion_z': motivacion_z,
                    'efectividad': efectividad,
                    'energia': energia
                }
            }
            
        except Exception as e:
            print(f"❌ Error en clasificación de microacción: {e}")
            return None
    
    def predecir_gratitud(self, usuario_id, dia, hora):
        """Predecir gratitud basada en usuario, día y hora"""
        if self.modelo_gratitudes is None:
            print("⚠️ Modelo de gratitudes no cargado. Ejecutar cargar_modelo_gratitudes() primero")
            return None
            
        try:
            # Preparar datos de entrada
            X_pred = np.array([[usuario_id, dia, hora]])
            
            # Hacer predicción
            prediccion = self.modelo_gratitudes.predict(X_pred)[0]
            probabilidades = self.modelo_gratitudes.predict_proba(X_pred)[0]
            
            gratitud_predicha = self.metadata_gratitudes['target_names'][prediccion]
            confianza = max(probabilidades) * 100
            
            return {
                'gratitud': gratitud_predicha,
                'confianza': confianza,
                'usuario_id': usuario_id,
                'dia': dia,
                'hora': hora
            }
            
        except Exception as e:
            print(f"❌ Error en predicción de gratitud: {e}")
            return None
    
    def predecir_estado_emocional(self, usuario_id, dia, hora):
        """Predecir estado emocional completo (felicidad, estrés, motivación)"""
        if self.modelos_prediccion_moodmaps is None:
            print("⚠️ Modelos de MoodMaps no cargados. Ejecutar cargar_modelo_moodmaps() primero")
            return None
            
        try:
            # Preparar datos de entrada
            X_pred = np.array([[usuario_id, dia, hora]])
            
            # Hacer predicciones para cada emoción
            predicciones = {}
            probabilidades = {}
            categorias = self.metadata_moodmaps['categorias_emocionales']
            
            for emocion in self.metadata_moodmaps['emociones_predichas']:
                pred = self.modelos_prediccion_moodmaps[emocion].predict(X_pred)[0]
                prob = self.modelos_prediccion_moodmaps[emocion].predict_proba(X_pred)[0]
                
                predicciones[emocion] = categorias[pred]
                probabilidades[emocion] = max(prob) * 100
            
            return {
                'predicciones': predicciones,
                'probabilidades': probabilidades,
                'usuario_id': usuario_id,
                'dia': dia,
                'hora': hora
            }
            
        except Exception as e:
            print(f"❌ Error en predicción de estado emocional: {e}")
            return None
    
    def clasificar_estado_emocional(self, felicidad, estres, motivacion, hora):
        """Clasificar estado emocional usando clustering"""
        if self.modelo_clustering_moodmaps is None or self.scaler_moodmaps is None:
            print("⚠️ Modelo de clustering de MoodMaps no cargado. Ejecutar cargar_modelo_moodmaps() primero")
            return None
            
        try:
            # Preparar datos de entrada
            X_input = np.array([[felicidad, estres, motivacion, hora]])
            X_scaled = self.scaler_moodmaps.transform(X_input)
            
            # Predecir cluster
            cluster = self.modelo_clustering_moodmaps.predict(X_scaled)[0]
            distancias = self.modelo_clustering_moodmaps.transform(X_scaled)[0]
            
            interpretacion = self.metadata_moodmaps['cluster_interpretations'][cluster]
            
            return {
                'cluster': int(cluster),
                'interpretacion': interpretacion,
                'distancias': distancias.tolist(),
                'estado_input': {
                    'felicidad': felicidad,
                    'estres': estres,
                    'motivacion': motivacion,
                    'hora': hora
                }
            }
            
        except Exception as e:
            print(f"❌ Error en clasificación de estado emocional: {e}")
            return None
    
    def cargar_todos_los_modelos(self):
        """Cargar todos los modelos disponibles"""
        print("Cargando todos los modelos disponibles...")
        
        resultados = {
            'emociones': self.cargar_modelo_emociones(),
            'microacciones': self.cargar_modelo_microacciones(),
            'gratitudes': self.cargar_modelo_gratitudes(),
            'moodmaps': self.cargar_modelo_moodmaps()
        }
        
        exitosos = sum(resultados.values())
        total = len(resultados)
        
        print(f"\nResumen: {exitosos}/{total} modelos cargados exitosamente")
        return exitosos == total
    
    def obtener_estadisticas(self):
        """Obtener estadísticas de todos los modelos cargados"""
        stats = {
            'modelos_cargados': 0,
            'total_modelos': 4,
            'detalles': {}
        }
        
        if self.modelo_emociones is not None:
            stats['modelos_cargados'] += 1
            stats['detalles']['emociones'] = {
                'tipo': 'RandomForestClassifier',
                'accuracy': self.metadata_emociones['accuracy'],
                'n_samples': self.metadata_emociones.get('n_samples', 'N/A'),
                'target_names': len(self.metadata_emociones['target_names'])
            }
        
        if self.modelo_clustering_microacciones is not None:
            stats['modelos_cargados'] += 1
            stats['detalles']['microacciones'] = {
                'tipo': 'KMeans Clustering',
                'n_clusters': self.metadata_clustering['n_clusters'],
                'n_samples': self.metadata_clustering.get('n_samples', 'N/A'),
                'features': len(self.metadata_clustering['feature_names'])
            }
        
        if self.modelo_gratitudes is not None:
            stats['modelos_cargados'] += 1
            stats['detalles']['gratitudes'] = {
                'tipo': 'RandomForestClassifier',
                'accuracy': self.metadata_gratitudes['accuracy'],
                'n_samples': self.metadata_gratitudes.get('n_samples', 'N/A'),
                'target_names': len(self.metadata_gratitudes['target_names'])
            }
        
        if self.modelo_clustering_moodmaps is not None:
            stats['modelos_cargados'] += 1
            stats['detalles']['moodmaps'] = {
                'tipo': 'KMeans + RandomForest',
                'accuracy_promedio': self.metadata_moodmaps['accuracy_promedio'],
                'n_clusters': self.metadata_moodmaps['n_clusters'],
                'n_samples': self.metadata_moodmaps.get('n_samples', 'N/A'),
                'emociones': len(self.metadata_moodmaps['emociones_predichas'])
            }
        
        return stats
    
    def demo_completo(self):
        """Ejecutar demo completo de todos los modelos"""
        print("🚀 DEMO COMPLETO DE MODELOS LUZ")
        print("="*60)
        
        # Cargar todos los modelos
        if not self.cargar_todos_los_modelos():
            print("❌ No se pudieron cargar todos los modelos")
            return False
        
        # Demo de emociones
        print("\n" + "="*50)
        print("DEMO: PREDICCIÓN DE EMOCIONES LIBERADAS")
        print("="*50)
        
        if self.modelo_emociones is not None:
            resultado_emocion = self.predecir_emocion(usuario_id=1, dia=5, hora=20)
            if resultado_emocion:
                print(f"Predicción para Usuario {resultado_emocion['usuario_id']}, Día {resultado_emocion['dia']}, {resultado_emocion['hora']}:00h:")
                print(f"   Emoción: {resultado_emocion['emocion']}")
                print(f"   Confianza: {resultado_emocion['confianza']:.1f}%")
        else:
            print("⚠️ Modelo de emociones no disponible")
        
        # Demo de microacciones
        print("\n" + "="*50)
        print("DEMO: CLUSTERING DE MICROACCIONES")
        print("="*50)
        
        if self.modelo_clustering_microacciones is not None:
            resultado_micro = self.clasificar_microaccion(
                felicidad_z=0.5, estres_z=-0.3, motivacion_z=0.8, 
                efectividad=4.2, energia=3.8
            )
            if resultado_micro:
                print(f"Clasificación de microacción:")
                print(f"   Cluster asignado: {resultado_micro['cluster']}")
                print(f"   Perfil emocional: {resultado_micro['perfil_emocional']}")
        else:
            print("⚠️ Modelo de microacciones no disponible")
        
        # Demo de gratitudes
        print("\n" + "="*50)
        print("DEMO: PREDICCIÓN DE GRATITUDES")
        print("="*50)
        
        if self.modelo_gratitudes is not None:
            resultado_gratitud = self.predecir_gratitud(usuario_id=2, dia=6, hora=21)
            if resultado_gratitud:
                print(f"Predicción para Usuario {resultado_gratitud['usuario_id']}, Día {resultado_gratitud['dia']}, {resultado_gratitud['hora']}:00h:")
                print(f"   Gratitud: {resultado_gratitud['gratitud']}")
                print(f"   Confianza: {resultado_gratitud['confianza']:.1f}%")
        else:
            print("⚠️ Modelo de gratitudes no disponible")
        
        # Demo de MoodMaps
        print("\n" + "="*50)
        print("DEMO: ANÁLISIS DE MOODMAPS")
        print("="*50)
        
        if self.modelos_prediccion_moodmaps is not None:
            # Predicción de estado emocional
            resultado_mood = self.predecir_estado_emocional(usuario_id=1, dia=5, hora=14)
            if resultado_mood:
                print(f"Predicción emocional para Usuario {resultado_mood['usuario_id']}, Día {resultado_mood['dia']}, {resultado_mood['hora']}:00h:")
                for emocion, nivel in resultado_mood['predicciones'].items():
                    confianza = resultado_mood['probabilidades'][emocion]
                    print(f"   {emocion.capitalize()}: {nivel} (confianza: {confianza:.1f}%)")
            
            # Clasificación de estado emocional
            resultado_cluster = self.clasificar_estado_emocional(felicidad=0.6, estres=0.3, motivacion=0.7, hora=15)
            if resultado_cluster:
                print(f"\nClasificación de estado emocional:")
                print(f"   Estado: {resultado_cluster['estado_input']}")
                print(f"   Cluster: {resultado_cluster['cluster']}")
                print(f"   Interpretación: {resultado_cluster['interpretacion']}")
        else:
            print("⚠️ Modelos de MoodMaps no disponibles")
        
        print("\n🎉 Demo completado exitosamente!")
        
        # Mostrar estadísticas finales
        stats = self.obtener_estadisticas()
        print(f"\nESTADÍSTICAS FINALES:")
        print(f"Modelos activos: {stats['modelos_cargados']}/{stats['total_modelos']}")
        
        return True

def main():
    """Función principal para ejecutar demo"""
    print("Inicializando sistema de modelos LUZ...")
    
    # Crear instancia de ModelosLUZ
    luz = ModelosLUZ()
    
    # Listar modelos disponibles
    luz.listar_modelos_disponibles()
    
    # Ejecutar demo completo
    luz.demo_completo()

if __name__ == "__main__":
    main()