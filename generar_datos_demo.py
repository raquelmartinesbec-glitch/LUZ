"""
Generador de datos ficticios para análisis de la app LUZ
Crea 7 días de datos realistas para 3 usuarios demo
"""

import requests
import json
import csv
import random
from datetime import datetime, timedelta
from typing import List, Dict
import os

# Configuración
BASE_URL = "http://localhost:8000"
USUARIOS_DEMO = [
    {"id": 1, "nombre": "Ana", "perfil": "Estudiante estresada"},
    {"id": 2, "nombre": "Carlos", "perfil": "Profesional ansioso"},
    {"id": 3, "nombre": "Luna", "perfil": "Artista creativa"}
]

# Patrones emocionales por usuario
PATRONES_EMOCIONALES = {
    1: {  # Ana - Estudiante estresada
        "felicidad": (0.3, 0.7),  # (min, max)
        "estres": (0.4, 0.9),
        "motivacion": (0.2, 0.6),
        "emociones_comunes": ["ansiedad", "frustración", "agobio", "presión", "cansancio"],
        "gratitudes": ["aprobar examen", "ayuda de amigos", "descanso", "café matutino", "música relajante"]
    },
    2: {  # Carlos - Profesional ansioso
        "felicidad": (0.2, 0.6),
        "estres": (0.5, 0.8),
        "motivacion": (0.3, 0.7),
        "emociones_comunes": ["estrés laboral", "presión", "agotamiento", "irritabilidad", "sobrecarga"],
        "gratitudes": ["tiempo en familia", "trabajo estable", "fin de semana", "ejercicio", "proyecto completado"]
    },
    3: {  # Luna - Artista creativa
        "felicidad": (0.4, 0.8),
        "estres": (0.1, 0.5),
        "motivacion": (0.5, 0.9),
        "emociones_comunes": ["bloqueo creativo", "autocrítica", "inseguridad", "dispersión"],
        "gratitudes": ["inspiración", "arte", "naturaleza", "colores", "nueva idea", "exposición"]
    }
}

# Microacciones disponibles
MICROACCIONES = [
    "respiración profunda", "caminata", "meditación", "música relajante",
    "ejercicio suave", "té caliente", "escribir gratitud", "estiramientos",
    "llamar amigo", "lectura", "arte/dibujo", "baño relajante"
]

def generar_timestamp_aleatorio(dia_offset: int, hora_min: int = 8, hora_max: int = 22):
    """Genera timestamp aleatorio para un día específico"""
    base_date = datetime.now() - timedelta(days=6-dia_offset)  # Últimos 7 días
    hora = random.randint(hora_min, hora_max)
    minuto = random.randint(0, 59)
    return base_date.replace(hour=hora, minute=minuto, second=0, microsecond=0)

def generar_moodmap(usuario_id: int):
    """Genera un estado emocional realista para un usuario"""
    patron = PATRONES_EMOCIONALES[usuario_id]
    
    return {
        "felicidad": round(random.uniform(*patron["felicidad"]), 2),
        "estres": round(random.uniform(*patron["estres"]), 2),
        "motivacion": round(random.uniform(*patron["motivacion"]), 2)
    }

def generar_datos_usuario(usuario_id: int, nombre: str, dias: int = 7):
    """Genera datos completos para un usuario durante N días"""
    datos_usuario = {
        "usuario_id": usuario_id,
        "nombre": nombre,
        "moodmaps": [],
        "emociones_liberadas": [],
        "gratitudes": [],
        "feedbacks": [],
        "estadisticas": {}
    }
    
    patron = PATRONES_EMOCIONALES[usuario_id]
    
    for dia in range(dias):
        # 2-4 registros MoodMap por día
        num_registros = random.randint(2, 4)
        
        for _ in range(num_registros):
            timestamp = generar_timestamp_aleatorio(dia)
            moodmap = generar_moodmap(usuario_id)
            
            datos_usuario["moodmaps"].append({
                "timestamp": timestamp.isoformat(),
                "dia": dia + 1,
                **moodmap
            })
            
            # Microacción sugerida y feedback (50% probabilidad)
            if random.random() < 0.5:
                microaccion = random.choice(MICROACCIONES)
                
                # Simular feedback realista
                efectividad = random.randint(2, 5)
                comodidad = random.randint(3, 5)
                energia = random.randint(1, 4)
                
                datos_usuario["feedbacks"].append({
                    "timestamp": timestamp.isoformat(),
                    "dia": dia + 1,
                    "microaccion": microaccion,
                    "efectividad": efectividad,
                    "comodidad": comodidad,
                    "energia": energia,
                    "moodmap_previo": moodmap
                })
        
        # Emociones liberadas (1-3 por día, más cuando hay más estrés)
        if random.random() < 0.7:  # 70% días con liberación
            num_emociones = random.randint(1, 3)
            for _ in range(num_emociones):
                emocion = random.choice(patron["emociones_comunes"])
                timestamp = generar_timestamp_aleatorio(dia, 19, 23)  # Más por la noche
                
                datos_usuario["emociones_liberadas"].append({
                    "timestamp": timestamp.isoformat(),
                    "dia": dia + 1,
                    "emocion": emocion
                })
        
        # Gratitudes (0-2 por día)
        if random.random() < 0.6:  # 60% días con gratitud
            num_gratitudes = random.randint(1, 2)
            for _ in range(num_gratitudes):
                gratitud = random.choice(patron["gratitudes"])
                timestamp = generar_timestamp_aleatorio(dia, 20, 23)  # Por la noche
                
                datos_usuario["gratitudes"].append({
                    "timestamp": timestamp.isoformat(),
                    "dia": dia + 1,
                    "gratitud": gratitud
                })
    
    # Calcular estadísticas
    if datos_usuario["moodmaps"]:
        felicidad_promedio = sum(m["felicidad"] for m in datos_usuario["moodmaps"]) / len(datos_usuario["moodmaps"])
        estres_promedio = sum(m["estres"] for m in datos_usuario["moodmaps"]) / len(datos_usuario["moodmaps"])
        motivacion_promedio = sum(m["motivacion"] for m in datos_usuario["moodmaps"]) / len(datos_usuario["moodmaps"])
        
        datos_usuario["estadisticas"] = {
            "total_registros_moodmap": len(datos_usuario["moodmaps"]),
            "total_emociones_liberadas": len(datos_usuario["emociones_liberadas"]),
            "total_gratitudes": len(datos_usuario["gratitudes"]),
            "total_feedbacks": len(datos_usuario["feedbacks"]),
            "felicidad_promedio": round(felicidad_promedio, 3),
            "estres_promedio": round(estres_promedio, 3),
            "motivacion_promedio": round(motivacion_promedio, 3),
            "microaccion_mas_usada": max(set([f["microaccion"] for f in datos_usuario["feedbacks"]]), 
                                       key=[f["microaccion"] for f in datos_usuario["feedbacks"]].count) if datos_usuario["feedbacks"] else "ninguna"
        }
    
    return datos_usuario

def exportar_datos_csv(todos_los_datos: List[Dict], carpeta_destino: str):
    """Exporta datos a archivos CSV para análisis"""
    os.makedirs(carpeta_destino, exist_ok=True)
    
    # CSV 1: Todos los MoodMaps
    moodmaps_csv = []
    for usuario in todos_los_datos:
        for moodmap in usuario["moodmaps"]:
            moodmaps_csv.append({
                "usuario_id": usuario["usuario_id"],
                "nombre": usuario["nombre"],
                "timestamp": moodmap["timestamp"],
                "dia": moodmap["dia"],
                "felicidad": moodmap["felicidad"],
                "estres": moodmap["estres"],
                "motivacion": moodmap["motivacion"]
            })
    
    with open(f"{carpeta_destino}/moodmaps.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["usuario_id", "nombre", "timestamp", "dia", "felicidad", "estres", "motivacion"])
        writer.writeheader()
        writer.writerows(moodmaps_csv)
    
    # CSV 2: Emociones liberadas
    emociones_csv = []
    for usuario in todos_los_datos:
        for emocion in usuario["emociones_liberadas"]:
            emociones_csv.append({
                "usuario_id": usuario["usuario_id"],
                "nombre": usuario["nombre"],
                "timestamp": emocion["timestamp"],
                "dia": emocion["dia"],
                "emocion": emocion["emocion"]
            })
    
    with open(f"{carpeta_destino}/emociones_liberadas.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["usuario_id", "nombre", "timestamp", "dia", "emocion"])
        writer.writeheader()
        writer.writerows(emociones_csv)
    
    # CSV 3: Gratitudes
    gratitudes_csv = []
    for usuario in todos_los_datos:
        for gratitud in usuario["gratitudes"]:
            gratitudes_csv.append({
                "usuario_id": usuario["usuario_id"],
                "nombre": usuario["nombre"],
                "timestamp": gratitud["timestamp"],
                "dia": gratitud["dia"],
                "gratitud": gratitud["gratitud"]
            })
    
    with open(f"{carpeta_destino}/gratitudes.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["usuario_id", "nombre", "timestamp", "dia", "gratitud"])
        writer.writeheader()
        writer.writerows(gratitudes_csv)
    
    # CSV 4: Feedbacks microacciones
    feedbacks_csv = []
    for usuario in todos_los_datos:
        for feedback in usuario["feedbacks"]:
            feedbacks_csv.append({
                "usuario_id": usuario["usuario_id"],
                "nombre": usuario["nombre"],
                "timestamp": feedback["timestamp"],
                "dia": feedback["dia"],
                "microaccion": feedback["microaccion"],
                "efectividad": feedback["efectividad"],
                "comodidad": feedback["comodidad"],
                "energia": feedback["energia"],
                "felicidad_previa": feedback["moodmap_previo"]["felicidad"],
                "estres_previo": feedback["moodmap_previo"]["estres"],
                "motivacion_previa": feedback["moodmap_previo"]["motivacion"]
            })
    
    with open(f"{carpeta_destino}/feedbacks_microacciones.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "usuario_id", "nombre", "timestamp", "dia", "microaccion", 
            "efectividad", "comodidad", "energia", 
            "felicidad_previa", "estres_previo", "motivacion_previa"
        ])
        writer.writeheader()
        writer.writerows(feedbacks_csv)
    
    # CSV 5: Estadísticas por usuario
    stats_csv = []
    for usuario in todos_los_datos:
        stats = usuario["estadisticas"]
        stats["usuario_id"] = usuario["usuario_id"]
        stats["nombre"] = usuario["nombre"]
        stats_csv.append(stats)
    
    with open(f"{carpeta_destino}/estadisticas_usuarios.csv", "w", newline="", encoding="utf-8") as f:
        fieldnames = ["usuario_id", "nombre"] + list(todos_los_datos[0]["estadisticas"].keys())
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(stats_csv)

def main():
    """Función principal"""
    print("🎭 Generando datos ficticios de LUZ para análisis...")
    print("=" * 60)
    
    todos_los_datos = []
    
    for usuario in USUARIOS_DEMO:
        print(f"📊 Generando datos para {usuario['nombre']} ({usuario['perfil']})...")
        datos = generar_datos_usuario(usuario["id"], usuario["nombre"])
        todos_los_datos.append(datos)
        
        stats = datos["estadisticas"]
        print(f"   ├── {stats['total_registros_moodmap']} registros MoodMap")
        print(f"   ├── {stats['total_emociones_liberadas']} emociones liberadas")
        print(f"   ├── {stats['total_gratitudes']} gratitudes")
        print(f"   └── {stats['total_feedbacks']} feedbacks microacciones")
        print()
    
    # Exportar datos completos como JSON
    carpeta_datos = "datos_demo_luz"
    os.makedirs(carpeta_datos, exist_ok=True)
    
    with open(f"{carpeta_datos}/datos_completos.json", "w", encoding="utf-8") as f:
        json.dump(todos_los_datos, f, indent=2, ensure_ascii=False)
    
    # Exportar CSVs para análisis
    print("💾 Exportando datos a CSV para análisis...")
    exportar_datos_csv(todos_los_datos, carpeta_datos)
    
    # Generar README para el análisis
    with open(f"{carpeta_datos}/README.md", "w", encoding="utf-8") as f:
        f.write("""# Datos Demo LUZ - 7 días de análisis

## Archivos generados:

### CSVs para análisis:
- `moodmaps.csv` - Todos los registros emocionales (felicidad, estrés, motivación)
- `emociones_liberadas.csv` - Emociones tóxicas liberadas en Alma Board
- `gratitudes.csv` - Microacciones de gratitud registradas
- `feedbacks_microacciones.csv` - Efectividad de microacciones sugeridas
- `estadisticas_usuarios.csv` - Resumen estadístico por usuario

### Datos completos:
- `datos_completos.json` - Todos los datos en formato JSON

## Usuarios demo:

1. **Ana** (ID: 1) - Estudiante estresada
   - Perfil: Altos niveles de estrés, motivación variable
   - Emociones típicas: ansiedad, frustración, agobio

2. **Carlos** (ID: 2) - Profesional ansioso  
   - Perfil: Estrés laboral, baja felicidad
   - Emociones típicas: estrés laboral, presión, agotamiento

3. **Luna** (ID: 3) - Artista creativa
   - Perfil: Alta motivación, bajo estrés, creativa
   - Emociones típicas: bloqueo creativo, autocrítica

## Período de datos: 
Últimos 7 días desde la fecha de generación.

## Sugerencias de análisis:
- Evolución emocional por usuario y día
- Efectividad de microacciones por tipo de usuario  
- Patrones de uso (horarios, frecuencia)
- Correlaciones entre liberación de emociones y mejora del mood
- Análisis de sentiment de gratitudes vs estado emocional
""")
    
    print("✅ ¡Datos generados exitosamente!")
    print(f"📂 Carpeta: {os.path.abspath(carpeta_datos)}")
    print("\n📋 Archivos creados:")
    for archivo in os.listdir(carpeta_datos):
        print(f"   └── {archivo}")
    
    # Mostrar estadísticas globales
    total_moodmaps = sum(len(u["moodmaps"]) for u in todos_los_datos)
    total_emociones = sum(len(u["emociones_liberadas"]) for u in todos_los_datos)
    total_gratitudes = sum(len(u["gratitudes"]) for u in todos_los_datos)
    total_feedbacks = sum(len(u["feedbacks"]) for u in todos_los_datos)
    
    print(f"\n📈 Estadísticas globales:")
    print(f"   ├── Total registros MoodMap: {total_moodmaps}")
    print(f"   ├── Total emociones liberadas: {total_emociones}")
    print(f"   ├── Total gratitudes: {total_gratitudes}")
    print(f"   └── Total feedbacks: {total_feedbacks}")

if __name__ == "__main__":
    main()