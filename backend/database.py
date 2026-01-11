"""
Configuración de la base de datos
Creación automática de tablas y gestión de conexiones
Soporta bases de datos separadas para producción y tests
"""

from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os
from datetime import datetime, timedelta

# Detectar si estamos en modo test
TEST_MODE = os.getenv("TEST_MODE", "false").lower() == "true"

# URLs de base de datos
if TEST_MODE:
    # Base de datos SQLite separada para tests (no altera datos reales)
    DATABASE_URL = os.getenv(
        "TEST_DATABASE_URL",
        "sqlite:///./luz_test.db"
    )
    print("⚠️  MODO TEST: Usando base de datos de test (luz_test.db)")
else:
    # Base de datos de producción (SQLite por defecto, o PostgreSQL)
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "sqlite:///./luz_bienestar.db"
    )

# Crear engine de SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
    echo=False  # Cambiar a True para debug SQL
)

# Crear SessionLocal para transacciones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base declarativa para los modelos
Base = declarative_base()


def get_db():
    """
    Dependency para obtener sesión de base de datos
    Se cierra automáticamente después de cada request
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def crear_tablas():
    """
    Crea todas las tablas definidas en los modelos
    Se ejecuta automáticamente al iniciar la aplicación
    """
    Base.metadata.create_all(bind=engine)
    print("✓ Tablas de base de datos creadas correctamente")


def limpiar_datos_antiguos(db: Session, dias: int = 90):
    """
    Elimina registros antiguos para mantener la base de datos ligera
    
    Args:
        db: Sesión de base de datos
        dias: Número de días de retención de datos
    """
    from models.db_models import FeedbackDB, HistoricoInteraccionDB
    
    fecha_limite = datetime.now() - timedelta(days=dias)
    
    # Eliminar feedbacks antiguos
    feedbacks_eliminados = db.query(FeedbackDB).filter(
        FeedbackDB.timestamp < fecha_limite
    ).delete()
    
    # Eliminar interacciones antiguas
    interacciones_eliminadas = db.query(HistoricoInteraccionDB).filter(
        HistoricoInteraccionDB.fecha < fecha_limite
    ).delete()
    
    db.commit()
    
    print(f"✓ Limpieza completada:")
    print(f"  - Feedbacks eliminados: {feedbacks_eliminados}")
    print(f"  - Interacciones eliminadas: {interacciones_eliminadas}")
    
    return {
        "feedbacks_eliminados": feedbacks_eliminados,
        "interacciones_eliminadas": interacciones_eliminadas
    }


def borrar_todas_las_tablas():
    """
    CUIDADO: Borra todas las tablas de la base de datos
    Usar solo para reset completo en desarrollo
    """
    Base.metadata.drop_all(bind=engine)
    print("⚠ Todas las tablas han sido eliminadas")
