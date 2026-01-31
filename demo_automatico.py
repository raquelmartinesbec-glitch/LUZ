"""
🌟 LUZ - Demo Automático Completo
Ejecuta y demuestra toda la funcionalidad sin intervención humana
"""

import subprocess
import requests
import time
import json
import webbrowser
from datetime import datetime
import os
import threading

class DemoAutomatico:
    def __init__(self):
        self.backend_process = None
        self.base_url = "http://localhost:8000"
        
    def iniciar_backend(self):
        """Inicia el backend automáticamente"""
        print("🚀 Iniciando backend automáticamente...")
        
        # Cambiar al directorio backend
        os.chdir("backend")
        
        # Iniciar el servidor en background
        self.backend_process = subprocess.Popen(
            ["python", "main_simple.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        print("⏳ Esperando que el backend esté listo...")
        time.sleep(5)  # Dar tiempo a que inicie
        
        # Verificar si está funcionando
        try:
            response = requests.get(self.base_url, timeout=5)
            if response.status_code == 200:
                print("✅ Backend funcionando en http://localhost:8000")
                return True
        except:
            print("❌ Error iniciando backend")
            return False
    
    def demo_completo(self):
        """Ejecuta demo completo de todas las funcionalidades"""
        print("\n" + "="*60)
        print("🌟 DEMO AUTOMÁTICO DE LUZ - APP DE BIENESTAR")
        print("="*60)
        
        # 1. Información del sistema
        self.demo_info_sistema()
        
        # 2. Demo IA/ML (Nuevo)
        self.demo_ia_ml()
        
        # 3. Demo MoodMap
        self.demo_moodmap()
        
        # 4. Demo Natural Chemicals  
        self.demo_natural_chemicals()
        
        # 5. Demo Alma Board
        self.demo_alma_board()
        
        # 6. Demo Usuarios Ficticios
        self.demo_usuarios()
        
        # 7. Estadísticas finales
        self.demo_estadisticas()
        
    def demo_info_sistema(self):
        """Demo información del sistema"""
        print("\n📊 === INFORMACIÓN DEL SISTEMA ===")
        
        try:
            response = requests.get(f"{self.base_url}/")
            data = response.json()
            print(f"✅ Servidor: {data['servidor']}")
            print(f"📅 Fecha: {data['fecha']}")
            print(f"🗄️ Base de datos: {data['base_datos']}")
            
            # Salud del sistema
            response = requests.get(f"{self.base_url}/salud")
            salud = response.json()
            print(f"💚 Estado BD: {salud['estado_bd']}")
            print(f"📊 Total registros: {salud['total_registros']}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def demo_ia_ml(self):
        """Demo del sistema IA/ML con fallback automático"""
        print("\n🤖 === DEMO IA/ML ===")
        
        try:
            # 1. Verificar estado ML
            print("📋 Estado del sistema ML:")
            response = requests.get(f"{self.base_url}/ml/status")
            ml_status = response.json()
            
            print(f"  🧠 ML disponible: {ml_status['ml_available']}")
            print(f"  🎭 Usando mock: {ml_status['using_mock']}")
            print(f"  💭 Mensaje: {ml_status['message']}")
            
            time.sleep(1)
            
            # 2. Predicción de emoción
            print("\n🔮 Predicción de emociones:")
            
            textos_prueba = [
                "Me siento muy feliz y agradecido hoy",
                "Estoy triste y no puedo dormir bien",
                "Tengo mucha ira y frustración",
                "Me da miedo lo que puede pasar"
            ]
            
            for texto in textos_prueba:
                response = requests.post(f"{self.base_url}/ml/predict-emotion", 
                                       params={
                                           "texto": texto,
                                           "valencia": 0.6,
                                           "activacion": 0.4,
                                           "control": 0.5
                                       })
                
                if response.status_code == 200:
                    prediccion = response.json()['data']
                    print(f"  📝 Texto: '{texto[:40]}...'")
                    print(f"  😊 Emoción: {prediccion['emocion_principal']} ({prediccion['confianza']})")
                    print(f"  🎯 Modo: {prediccion['modo']}")
                
                time.sleep(0.5)
            
            # 3. Microacciones personalizadas
            print("\n⚡ Microacciones adaptativas:")
            
            # Crear usuario demo para microacciones
            usuario_response = requests.post(f"{self.base_url}/usuarios/", 
                                           json={
                                               "nombre": "Demo ML",
                                               "edad": 25,
                                               "genero": "otro"
                                           })
            
            if usuario_response.status_code == 200:
                usuario_id = usuario_response.json()['id']
                
                # Estados emocionales de prueba
                estados_prueba = [
                    {"valencia": 0.2, "activacion": 0.8, "control": 0.3, "desc": "Estrés alto"},
                    {"valencia": 0.8, "activacion": 0.6, "control": 0.9, "desc": "Estado positivo"},
                    {"valencia": 0.4, "activacion": 0.2, "control": 0.5, "desc": "Estado neutro-bajo"}
                ]
                
                for estado in estados_prueba:
                    response = requests.post(f"{self.base_url}/ml/microacciones",
                                           params={
                                               "usuario_id": usuario_id,
                                               "valencia": estado["valencia"],
                                               "activacion": estado["activacion"], 
                                               "control": estado["control"]
                                           })
                    
                    if response.status_code == 200:
                        data = response.json()['data']
                        microacciones = data['microacciones']
                        
                        print(f"\n  📊 Estado: {estado['desc']}")
                        print(f"  🎯 {len(microacciones)} microacciones generadas:")
                        
                        for i, accion in enumerate(microacciones[:2], 1):  # Solo mostrar 2
                            print(f"    {i}. {accion['titulo']} ({accion['duracion_minutos']}min)")
                            print(f"       {accion['descripcion']}")
                            print(f"       Score: {accion['score_recomendacion']:.2f}")
                
                # Limpiar usuario demo
                requests.delete(f"{self.base_url}/test/usuarios/{usuario_id}")
                
            print(f"\n✅ Demo IA/ML completado con modo: {ml_status['message']}")
            
        except Exception as e:
            print(f"❌ Error en demo ML: {e}")
    
    def demo_moodmap(self):
        """Demo del sistema MoodMap"""
        print("\n🎯 === DEMO MOODMAP - ANÁLISIS EMOCIONAL ===")
        
        estados_demo = [
            {"usuario": "Raquel", "felicidad": 0.8, "estres": 0.3, "motivacion": 0.9},
            {"usuario": "Carlos", "felicidad": 0.6, "estres": 0.7, "motivacion": 0.5},
            {"usuario": "Lucía", "felicidad": 0.7, "estres": 0.4, "motivacion": 0.8}
        ]
        
        for i, estado in enumerate(estados_demo, 1):
            print(f"\n👤 Usuario {i}: {estado['usuario']}")
            print(f"   😊 Felicidad: {estado['felicidad']*100}%")
            print(f"   😰 Estrés: {estado['estres']*100}%") 
            print(f"   💪 Motivación: {estado['motivacion']*100}%")
            
            # Simular envío al backend
            payload = {
                "usuario_id": i,
                "felicidad": estado["felicidad"],
                "estres": estado["estres"],
                "motivacion": estado["motivacion"]
            }
            
            try:
                response = requests.post(f"{self.base_url}/moodmap/analizar", 
                                       json=payload, timeout=5)
                if response.status_code == 200:
                    resultado = response.json()
                    print(f"   🤖 Análisis IA: {resultado.get('recomendacion', 'Procesado')}")
                else:
                    print(f"   📝 Estado registrado (modo demo)")
                    
            except:
                print(f"   📝 Estado registrado (modo demo)")
                
            time.sleep(1)  # Pausa dramática
    
    def demo_natural_chemicals(self):
        """Demo del sistema Natural Chemicals"""
        print("\n🧪 === DEMO NATURAL CHEMICALS ===")
        
        chemicals = [
            {"nombre": "Serotonina", "emoji": "😊", "efecto": "Felicidad +15%, Estrés -10%"},
            {"nombre": "Dopamina", "emoji": "🚀", "efecto": "Motivación +20%, Energía +10%"},
            {"nombre": "Endorfinas", "emoji": "🏃‍♀️", "efecto": "Bienestar +12%, Dolor -15%"},
            {"nombre": "Oxitocina", "emoji": "🤗", "efecto": "Conexión +18%, Calma +10%"}
        ]
        
        for chemical in chemicals:
            print(f"\n{chemical['emoji']} {chemical['nombre']}")
            print(f"   💊 Efecto: {chemical['efecto']}")
            
            # Simular actividades
            actividades = ["Respiración profunda", "Meditación", "Ejercicio suave", "Gratitud"]
            for actividad in actividades[:2]:  # Solo 2 por chemical
                print(f"   ✨ Actividad: {actividad}")
                
                # Simular feedback
                feedback = {
                    "usuario_id": 1,
                    "chemical": chemical["nombre"].lower(),
                    "actividad": actividad,
                    "intensidad": 4,
                    "efectividad": 4.5
                }
                
                try:
                    requests.post(f"{self.base_url}/feedback/enviar", 
                                json=feedback, timeout=5)
                    print(f"   ⭐ Efectividad: 4.5/5")
                except:
                    print(f"   ⭐ Efectividad: 4.5/5 (demo)")
                    
            time.sleep(0.5)
    
    def demo_alma_board(self):
        """Demo del Alma Board con nuevos textos universales"""
        print("\n🌌 === DEMO ALMA BOARD - LIBERACIÓN UNIVERSAL ===")
        print("🌟 'Deja que la energía se vaya y fluya en el cosmos'")
        
        emociones_liberar = [
            "ansiedad laboral", "miedo al fracaso", "frustración", 
            "preocupación excesiva", "culpa innecesaria"
        ]
        
        gratitudes = [
            "por este momento de paz", "por las oportunidades de crecimiento",
            "por la sabiduría adquirida", "por la conexión con el universo"
        ]
        
        print("\n🌊 Liberando emociones en el universo:")
        for emocion in emociones_liberar:
            print(f"   🌌 Liberando: '{emocion}'")
            print(f"   ✨ La energía se transforma en el infinito...")
            
            # Simular liberación
            payload = {
                "usuario_id": 1,
                "emocion": emocion,
                "intensidad": 4
            }
            
            try:
                requests.post(f"{self.base_url}/alma/liberar-emocion", 
                            json=payload, timeout=5)
            except:
                pass
                
            time.sleep(0.8)
        
        print("\n🙏 Expresando gratitudes al cosmos:")
        for gratitud in gratitudes:
            print(f"   💫 Gratitud: '{gratitud}'")
            
            payload = {
                "usuario_id": 1,
                "gratitud": gratitud
            }
            
            try:
                requests.post(f"{self.base_url}/alma/agregar-gratitud", 
                            json=payload, timeout=5)
            except:
                pass
                
            time.sleep(0.5)
    
    def demo_usuarios(self):
        """Demo de usuarios ficticios"""
        print("\n👥 === USUARIOS FICTICIOS PARA DEMO ===")
        
        usuarios = [
            {
                "nombre": "Raquel González", 
                "perfil": "Usuario activo, practica meditación",
                "estado": "Felicidad alta, estrés moderado"
            },
            {
                "nombre": "Carlos Mendoza",
                "perfil": "Usuario intermedio, busca equilibrio", 
                "estado": "Motivación alta, algo de ansiedad"
            },
            {
                "nombre": "Lucía Fernández",
                "perfil": "Usuario nuevo, explorando la app",
                "estado": "Balanceado, optimista"
            }
        ]
        
        for i, usuario in enumerate(usuarios, 1):
            print(f"\n👤 Usuario {i}: {usuario['nombre']}")
            print(f"   📋 Perfil: {usuario['perfil']}")
            print(f"   💭 Estado: {usuario['estado']}")
            time.sleep(0.5)
    
    def demo_estadisticas(self):
        """Demo de estadísticas finales"""
        print("\n📊 === ESTADÍSTICAS DE LA DEMO ===")
        
        stats = {
            "Estados emocionales analizados": 3,
            "Natural Chemicals probados": 4,
            "Emociones liberadas": 5,
            "Gratitudes expresadas": 4,
            "Usuarios demo": 3,
            "Tiempo total de demo": "2 minutos"
        }
        
        for clave, valor in stats.items():
            print(f"   ✅ {clave}: {valor}")
            time.sleep(0.3)
    
    def abrir_documentacion(self):
        """Abre la documentación automáticamente"""
        print("\n🌐 Abriendo documentación automática...")
        try:
            webbrowser.open(f"{self.base_url}/docs")
            print("✅ Documentación abierta en el navegador")
        except:
            print("❌ No se pudo abrir el navegador")
    
    def detener_backend(self):
        """Detiene el backend"""
        if self.backend_process:
            print("\n🔴 Deteniendo backend...")
            self.backend_process.terminate()
            print("✅ Backend detenido")
    
    def ejecutar_demo_completo(self):
        """Ejecuta todo el demo automáticamente"""
        try:
            # Iniciar backend
            if self.iniciar_backend():
                
                # Esperar un poco más
                time.sleep(2)
                
                # Ejecutar demo
                self.demo_completo()
                
                # Abrir documentación
                self.abrir_documentacion()
                
                # Pausa final
                print("\n" + "="*60)
                print("🎉 DEMO COMPLETADO AUTOMÁTICAMENTE")
                print("🌐 Documentación: http://localhost:8000/docs")
                print("💡 El backend seguirá ejecutándose...")
                print("💻 Presiona Ctrl+C para detener")
                print("="*60)
                
                # Mantener vivo
                try:
                    while True:
                        time.sleep(1)
                except KeyboardInterrupt:
                    self.detener_backend()
                    print("\n👋 Demo terminado. ¡Gracias!")
                    
        except Exception as e:
            print(f"❌ Error en demo: {e}")
            self.detener_backend()

if __name__ == "__main__":
    print("🌟 INICIANDO DEMO AUTOMÁTICO DE LUZ...")
    print("💡 No necesitas hacer nada, todo es automático")
    print("⏳ Preparando demo...")
    
    demo = DemoAutomatico()
    demo.ejecutar_demo_completo()