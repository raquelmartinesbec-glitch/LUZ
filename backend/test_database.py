"""
Script de prueba para verificar la base de datos
Usa una base de datos SQLite separada (luz_test.db) que NO altera los datos reales
Ejecutar: python test_database.py
"""

import sys
import os
sys.path.append('.')

# IMPORTANTE: Activar modo test ANTES de importar database
os.environ["TEST_MODE"] = "true"

from database import crear_tablas, get_db, borrar_todas_las_tablas
from models.db_models import UsuarioDB, MoodMapDB, FeedbackDB
from utils.db_utils import obtener_estadisticas_db, limpiar_por_antigüedad

def test_crear_tablas():
    """Prueba la creación de tablas"""
    print("\n🧪 Test 1: Creación de tablas")
    print("-" * 50)
    
    try:
        crear_tablas()
        print("✓ Tablas creadas correctamente en luz_test.db")
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_insertar_datos():
    """Prueba la inserción de datos"""
    print("\n🧪 Test 2: Inserción de datos")
    print("-" * 50)
    
    try:
        db = next(get_db())
        
        # Crear usuario de prueba
        usuario = UsuarioDB(
            nombre="Usuario Test",
            avatar="test.png"
        )
        db.add(usuario)
        db.commit()
        db.refresh(usuario)
        
        print(f"✓ Usuario creado con ID: {usuario.id}")
        
        # Crear MoodMap de prueba
        moodmap = MoodMapDB(
            usuario_id=usuario.id,
            felicidad=0.8,
            estres=0.3,
            motivacion=0.9
        )
        db.add(moodmap)
        db.commit()
        
        print(f"✓ MoodMap creado")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_consultar_datos():
    """Prueba la consulta de datos"""
    print("\n🧪 Test 3: Consulta de datos")
    print("-" * 50)
    
    try:
        db = next(get_db())
        
        # Contar usuarios
        total_usuarios = db.query(UsuarioDB).count()
        print(f"✓ Total de usuarios: {total_usuarios}")
        
        # Contar MoodMaps
        total_moodmaps = db.query(MoodMapDB).count()
        print(f"✓ Total de MoodMaps: {total_moodmaps}")
        
        # Obtener estadísticas
        stats = obtener_estadisticas_db(db)
        print(f"✓ Estadísticas obtenidas: {stats}")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_limpieza_datos():
    """Prueba la limpieza de datos antiguos"""
    print("\n🧪 Test 4: Limpieza de datos")
    print("-" * 50)
    
    try:
        db = next(get_db())
        
        resultado = limpiar_por_antigüedad(db, dias_retencion=90)
        print(f"✓ Limpieza completada: {resultado}")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def limpiar_bd_test():
    """Limpia la base de datos de prueba"""
    print("\n🧹 Limpiando base de datos de prueba...")
    print("-" * 50)
    
    try:
        borrar_todas_las_tablas()
        print("✓ Base de datos limpiada")
    except Exception as e:
        print(f"✗ Error: {e}")


def main():
    """Ejecuta todos los tests"""
    print("\n" + "=" * 50)
    print("🌟 Tests de Base de Datos - Luz")
    print("=" * 50)
    
    resultados = []
    
    # Test 1: Crear tablas
    resultados.append(("Crear tablas", test_crear_tablas()))
    
    # Test 2: Insertar datos
    resultados.append(("Insertar datos", test_insertar_datos()))
    
    # Test 3: Consultar datos
    resultados.append(("Consultar datos", test_consultar_datos()))
    
    # Test 4: Limpieza
    resultados.append(("Limpieza datos", test_limpieza_datos()))
    
    # Resumen
    print("\n" + "=" * 50)
    print("📊 Resumen de Tests")
    print("=" * 50)
    
    tests_exitosos = sum(1 for _, resultado in resultados if resultado)
    total_tests = len(resultados)
    
    for nombre, resultado in resultados:
        status = "✓ PASS" if resultado else "✗ FAIL"
        print(f"{status} - {nombre}")
    
    print("\n" + "-" * 50)
    print(f"Total: {tests_exitosos}/{total_tests} tests exitosos")
    print("=" * 50 + "\n")
    
    # Preguntar si limpiar
    print("💡 NOTA: Los tests usan luz_test.db (base de datos separada)")
    print("   Los datos reales en luz_bienestar.db NO fueron alterados")
    respuesta = input("\n¿Deseas limpiar la base de datos de prueba? (s/n): ")
    if respuesta.lower() == 's':
        limpiar_bd_test()
    
    return tests_exitosos == total_tests


if __name__ == "__main__":
    exito = main()
    sys.exit(0 if exito else 1)
