"""
Demo rápido para probar endpoints ML sin reiniciar backend
"""

import requests
import json

def test_ml_endpoints():
    base_url = "http://localhost:8000"
    
    print("🧪 Probando endpoints ML...")
    
    try:
        # 1. Estado ML
        print("\n1️⃣ Estado ML:")
        response = requests.get(f"{base_url}/ml/status")
        if response.status_code == 200:
            data = response.json()
            print(f"   ML disponible: {data['ml_available']}")
            print(f"   Usando mock: {data['using_mock']}")
            print(f"   Mensaje: {data['message']}")
        else:
            print(f"   ❌ Error: {response.status_code}")
            
        # 2. Predicción de emoción
        print("\n2️⃣ Predicción de emoción:")
        response = requests.post(f"{base_url}/ml/predict-emotion", 
                               params={
                                   "texto": "Me siento muy feliz hoy",
                                   "valencia": 0.8,
                                   "activacion": 0.7,
                                   "control": 0.6
                               })
        if response.status_code == 200:
            data = response.json()['data']
            print(f"   Emoción: {data['emocion_principal']}")
            print(f"   Confianza: {data['confianza']}")
            print(f"   Modo: {data['modo']}")
        else:
            print(f"   ❌ Error: {response.status_code}")
            
        print("\n✅ Prueba completada")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_ml_endpoints()