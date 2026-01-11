# Backend - Luz API

## Instalación

### 1. Crear entorno virtual

```powershell
python -m venv venv
```

### 2. Activar entorno virtual

**Windows PowerShell:**
```powershell
.\venv\Scripts\Activate
```

**Windows CMD:**
```cmd
venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 3. Instalar dependencias

```powershell
pip install -r requirements.txt
```

### 4. Ejecutar servidor

```powershell
python main.py
```

El servidor estará disponible en: `http://localhost:8000`

## Documentación API

Una vez el servidor esté ejecutándose, accede a:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Estructura

```
backend/
├── main.py                 # Aplicación FastAPI principal
├── database.py             # Configuración de BD y creación automática
├── models/
│   ├── usuario.py         # Modelos Pydantic (API)
│   └── db_models.py       # Modelos SQLAlchemy (BD)
├── services/
│   ├── ia_service.py      # IA: RandomForest, Red Neuronal, Clustering
│   ├── rl_service.py      # Reinforcement Learning (Q-Learning)
│   └── nlp_service.py     # NLP y generación de frases
├── utils/
│   └── db_utils.py        # Utilidades de BD y limpieza
├── test_database.py        # Tests de base de datos
└── requirements.txt        # Dependencias Python
```

## Base de Datos Automática ✨

### Creación Automática de Tablas
Las tablas se crean automáticamente al iniciar el servidor. No necesitas ejecutar scripts SQL manualmente.

**Tablas creadas:**
- `usuarios` - Información de usuarios
- `moodmaps` - Estados emocionales
- `feedbacks` - Evaluaciones de microacciones
- `historico_interacciones` - Registro completo de interacciones
- `emociones_liberadas` - Emociones del Alma Board
- `gratitudes` - Microacciones de gratitud
- `destellos` - Destellos de luz generados
- `configuracion_rl` - Q-Table del RL

### Limpieza Automática de Datos
Al iniciar el servidor, se eliminan automáticamente:
- Feedbacks antiguos (>90 días)
- Interacciones antiguas (>90 días)
- Emociones liberadas (>180 días)
- Gratitudes antiguas (>180 días)
- Destellos (>30 días)

## Servicios de IA

### IAService
- RandomForest para clasificación de estados emocionales
- Red neuronal ligera (autoencoder) para embeddings latentes
- KMeans para clustering de patrones emocionales
- Entrenamiento continuo con feedback de usuarios

### RLService
- Q-Learning simplificado para selección de microacciones
- Política ε-greedy (exploración vs explotación)
- Actualización continua con recompensas
- Historial de efectividad por acción

### NLPService
- sentence-transformers para embeddings de texto
- Análisis de sentimiento
- Generación de frases motivadoras estilo boho chic zen
- Categorización de emociones

## Endpoints Principales

### MoodMap
```http
POST /moodmap/analizar
Content-Type: application/json

{
  "felicidad": 0.7,
  "estres": 0.3,
  "motivacion": 0.8
}
```

### Feedback
```http
POST /feedback/enviar
Content-Type: application/json

{
  "usuario_id": 1,
  "microaccion": "calmarse",
  "efectividad": 4.5,
  "comodidad": 4.0,
  "energia": 3.5,
  "comentario_texto": "Me ayudó mucho a relajarme",
  "moodmap_previo": {
    "felicidad": 0.5,
    "estres": 0.7,
    "motivacion": 0.4
  }
}
```

## Notas

- Los modelos de IA se inicializan con datos sintéticos
- El sistema aprende continuamente con el feedback de usuarios
- **Las tablas se crean automáticamente** al iniciar el servidor
- **Limpieza automática** de datos antiguos en cada inicio
- En producción, configurar PostgreSQL para histórico
- Ajustar CORS según dominios específicos

## Tests

Para verificar que la base de datos funciona correctamente:

```powershell
python test_database.py
```

Esto ejecutará tests de:
- Creación de tablas
- Inserción de datos
- Consultas
- Limpieza automática

## Mantenimiento Manual

Aunque la limpieza es automática, puedes ejecutarla manualmente:

```http
POST /mantenimiento/limpiar?dias_retencion=90
```

Optimizar base de datos:

```http
POST /mantenimiento/optimizar
```
