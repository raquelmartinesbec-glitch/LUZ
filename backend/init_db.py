"""
Script para inicializar la base de datos y crear usuarios de prueba
Ejecutar: python init_db.py
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import crear_tablas, get_db, SessionLocal
from utils.test_users import crear_usuario_test
from models.db_models import UsuarioDB
import json

def crear_usuarios_ficticios():
    """Crea los 3 usuarios ficticios para la demo"""
    
    # Usuarios ficticios definidos
    usuarios_ficticios = [
        {
            "nombre": "Elena Serenidad",
            "avatar": "avatar_elena.png",
            "descripcion": "Usuario demo - Profesional urbana que busca equilibrio"
        },
        {
            "nombre": "Marco Equilibrio", 
            "avatar": "avatar_marco.png",
            "descripcion": "Usuario demo - Estudiante que maneja estrés académico"
        },
        {
            "nombre": "Luna Gratitud",
            "avatar": "avatar_luna.png", 
            "descripcion": "Usuario demo - Artista enfocada en mindfulness"
        }
    ]
    
    db = SessionLocal()
    usuarios_creados = []
    
    try:
        print("🔧 Creando usuarios ficticios...")
        
        for user_data in usuarios_ficticios:
            # Verificar si ya existe
            usuario_existente = db.query(UsuarioDB).filter(
                UsuarioDB.nombre == user_data["nombre"]
            ).first()
            
            if usuario_existente:
                print(f"   ✓ Usuario '{user_data['nombre']}' ya existe (ID: {usuario_existente.id})")
                usuarios_creados.append({
                    "id": usuario_existente.id,
                    "nombre": usuario_existente.nombre,
                    "avatar": usuario_existente.avatar,
                    "existe": True
                })
            else:
                # Crear nuevo usuario
                nuevo_usuario = UsuarioDB(
                    nombre=user_data["nombre"],
                    avatar=user_data["avatar"]
                )
                db.add(nuevo_usuario)
                db.flush()
                
                print(f"   ✓ Usuario '{user_data['nombre']}' creado (ID: {nuevo_usuario.id})")
                usuarios_creados.append({
                    "id": nuevo_usuario.id,
                    "nombre": nuevo_usuario.nombre,
                    "avatar": nuevo_usuario.avatar,
                    "existe": False
                })
        
        db.commit()
        
        return usuarios_creados
        
    except Exception as e:
        print(f"❌ Error creando usuarios: {e}")
        db.rollback()
        return []
    finally:
        db.close()


def crear_usuario_postman():
    """Crea un usuario de prueba específico para Postman"""
    db = SessionLocal()
    try:
        resultado = crear_usuario_test(
            db=db,
            nombre="Test Postman API",
            avatar="test_postman.png",
            tipo_test="postman",
            descripcion="Usuario para testing de API con Postman"
        )
        return resultado
    finally:
        db.close()


def main():
    print("🚀 Inicializando base de datos de Luz Bienestar")
    print("=" * 60)
    
    # 1. Crear tablas
    print("📊 Creando estructura de base de datos...")
    crear_tablas()
    
    # 2. Crear usuarios ficticios
    usuarios_demo = crear_usuarios_ficticios()
    
    # 3. Crear usuario de Postman
    print("\n🧪 Creando usuario de prueba para Postman...")
    try:
        usuario_postman = crear_usuario_postman()
        print(f"   ✓ Usuario Postman creado (ID: {usuario_postman['usuario_id']})")
    except Exception as e:
        print(f"   ⚠ Error creando usuario Postman: {e}")
        usuario_postman = None
    
    # 4. Resumen
    print("\n" + "=" * 60)
    print("✨ INICIALIZACIÓN COMPLETADA")
    print("=" * 60)
    
    print("\n📱 Usuarios Demo (para Flutter frontend):")
    for user in usuarios_demo:
        status = "existe" if user.get("existe") else "nuevo"
        print(f"   • {user['nombre']} (ID: {user['id']}) - {status}")
    
    if usuario_postman:
        print(f"\n🧪 Usuario Postman (para testing API):")
        print(f"   • ID: {usuario_postman['usuario_id']}")
        print(f"   • Nombre: {usuario_postman['nombre']}")
        print(f"   • Usar este ID en tus requests de Postman")
    
    print("\n🌐 Servidor backend:")
    print("   • Ejecuta: python main.py")
    print("   • API disponible en: http://localhost:8000")
    print("   • Documentación: http://localhost:8000/docs")
    
    print("\n📱 Frontend Flutter:")
    print("   • Directorio: ../frontend")
    print("   • Instalar deps: flutter pub get")
    print("   • Ejecutar: flutter run")


if __name__ == "__main__":
    main()