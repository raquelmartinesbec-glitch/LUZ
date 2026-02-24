# 🌟 Luz - App de Bienestar Interactiva

**Prototipo completo de aplicación de bienestar con IA adaptativa**

Estilo: Boho Chic Zen · Frontend: Flutter · Backend: FastAPI + IA/ML

## 🚀 TL;DR - Lo Esencial del Proyecto

### ¿Qué es Luz?
**App de Bienestar con IA que personaliza recomendaciones según tu estado emocional**

- 📱 **Frontend:** Flutter (iOS/Android) con diseño Boho Chic Zen
- 🧠 **Backend:** FastAPI + 5 algoritmos de IA/ML (TensorFlow, scikit-learn)
- 🎯 **Objetivo:** MoodMap interactivo + Alma Board + Microacciones adaptativas

### ✨ Características Únicas

- 🎭 **MoodMap Board:** Burbujas emocionales animadas que visualizan tu estado
- 🌟 **Natural Chemicals:** Sistema revolucionario de químicos naturales (Serotonina, Dopamina, Endorfinas, Oxitocina)
- 🎪 **Alma Board:** Libera emociones tóxicas con drag & drop + destellos espectaculares
- 🤖 **IA Adaptativa:** 5 algoritmos que aprenden de ti (Random Forest + Neural Network + Q-Learning + NLP + Clustering)
- � **Seguimiento Post-Microacción:** Sistema automático que mide efectividad real de las actividades
- 📊 **Sistema Inteligente:** Archivado automático para investigación + limpieza periódica
- ⏰ **Recordatorios Inteligentes:** Notificaciones para capturar estado emocional después de cada microacción

### 🏃‍♂️ Inicio Rápido (2 opciones)

#### Opción A: Docker (Recomendado - ML completo)
```bash
git clone <repo-url> && cd LUZ
docker-compose up --build
# ✅ Backend: http://localhost:8000/docs
```

#### Opción B: Local (Funciona siempre - fallback automático)
```bash
# Backend (auto-detecta TensorFlow)
cd backend && pip install -r requirements.txt && python main.py
# ✅ Servidor: http://localhost:8000

# Frontend
cd frontend && flutter pub get && flutter run
# ✅ App móvil funcionando
```

### 🧠 IA/ML en Acción

**4 Modelos Entrenados y Evaluados:**
- **🙏 Gratitudes:** RandomForest, 23 muestras, 14 clases ⚠️ (Overfitting detectado - 100% accuracy)
- **😤 Emociones Liberadas:** RandomForest, 40.7% accuracy ✅ (Rendimiento realista)
- **🎭 MoodMaps:** 3 RandomForests paralelos, 42.5% accuracy promedio ✅ (Multi-dimensional)
- **⚡ Microacciones:** KMeans Clustering, 3 clusters identificados ✅ (Exploración de patrones)

**Características del Sistema:**
- **Análisis Crítico Completo:** Evaluación técnica honesta de fortalezas y debilidades
- **Sistema de Carga:** Utilidad unificada para cargar y usar todos los modelos
- **Validación Robusta:** Métricas realistas, detección de overfitting
- **Fallback Inteligente:** Mocks automáticos si TensorFlow no disponible

### 🎨 Demo con 3 Usuarios Ficticios

- **Raquel:** Meditadora activa (alta felicidad, estrés moderado)
- **Carlos:** Busca equilibrio (motivación alta, algo de ansiedad)  
- **Lucía:** Explorando la app (balanceada, optimista)

### 📊 Métricas del Proyecto

- **Código:** 5,700+ líneas (2,500 Dart + 3,200 Python)
- **IA/ML:** 4 modelos entrenados + sistema de evaluación crítica
- **Modelos Guardados:** 13 archivos .pkl con metadatos y métricas
- **Análisis Completos:** 4 notebooks Jupyter con análisis detallado
- **BD:** 11 tablas (8 operativas + 3 archivo permanente)
- **API:** 15+ endpoints documentados automáticamente
- **UI:** 3 pantallas + 7 widgets especializados + animaciones avanzadas

**Sistema ML Demo:** ✅ Modelos entrenados con datos sintéticos, evaluación crítica incluida  
**¿Sin TensorFlow?** ✅ No problem! Sistema de fallback automático con mocks inteligentes  
**¿Para Git?** ✅ Optimizado! Un comando Docker y funciona  
**¿Para desarrollo?** ✅ Hot reload + documentación interactiva + tests separados

---

## 🚀 **Quick Start (Para quien clona este repo)**

```bash
# 1️⃣ Clonar y entrar
git clone <repository-url>
cd LUZ

# 2️⃣ Ejecutar con Docker (recomendado)
docker-compose up --build

# 3️⃣ Abrir en el navegador
# Backend API: http://localhost:8000/docs  
# Frontend App: http://localhost:3000 (si usas profile dev)
```

**¿No tienes Docker?** Ve a [Instalación Local](#️-opción-2-instalación-local)

---

## 📋 Índice

- [TL;DR - Lo Esencial](#-tldr---lo-esencial-del-proyecto)
- [Quick Start](#-quick-start-para-quien-clona-este-repo)
- [Descripción](#-descripción)
- [Características](#-características)
- [Tecnologías](#-tecnologías)
- [Instalación](#-instalación)
- [API Endpoints](#-api-endpoints)

---

## 🎯 Descripción

**Luz** es una aplicación de bienestar que combina visualización emocional, microacciones adaptativas y liberación de emociones tóxicas. Utiliza Machine Learning para personalizar las recomendaciones según el estado emocional del usuario.

### Pantallas Principales

1. **MoodMap Board** - Visualización interactiva de emociones con burbujas animadas
2. **Alma Board** - Espacio para liberar emociones tóxicas y expresar gratitud
3. **Destellos de Luz** - Feedback visual personalizable con animaciones

---

## ✨ Características

### Frontend (Flutter)

- ✅ **3 Pantallas principales:** MoodMap Board, Alma Board, Destellos de Luz
- ✅ **Natural Chemicals:** Serotonina, Dopamina, Endorfinas, Oxitocina con intensidades 1-5
- ✅ **Tema Boho Chic Zen** con degradados, sombras y animaciones suaves
- ✅ **3 usuarios ficticios** para demo completa
- ✅ **Indicadores IA Online/Offline** en tiempo real

### Backend (FastAPI + IA/ML)

- ✅ **4 Modelos ML Entrenados y Evaluados**:
  - **🙏 Gratitudes:** RandomForest (100% accuracy - overfitting detectado)
  - **😤 Emociones Liberadas:** RandomForest (40.7% accuracy - realista)
  - **🎭 MoodMaps:** 3 RandomForests paralelos (42.5% promedio - multi-dimensional)
  - **⚡ Microacciones:** KMeans Clustering (3 clusters - exploración)

- ✅ **Sistema de Evaluación Crítica:** Análisis técnico completo en notebook
- ✅ **Carga Unificada de Modelos:** Utilidad para usar todos los modelos entrenados
- ✅ **Base de datos automática:** 11 tablas SQLite auto-creadas
- ✅ **Sistema de fallback:** Mocks inteligentes si TensorFlow no está disponible
- ✅ **Archivado automático:** Datos históricos preservados para investigación
- ✅ **Limpieza periódica:** Optimización automática mensual

---

## 🛠 Tecnologías

### Frontend
```yaml
Flutter: 3.0+
State Management: Riverpod 2.4.9
UI: Google Fonts (Cormorant, Montserrat, Lato)
Animaciones: AnimationController, CustomPainter
```

### Backend
```yaml
Framework: FastAPI 0.109.0
IA/ML: 
  - TensorFlow 2.16.1
  - scikit-learn 1.4.0
  - pandas 2.2.0
  - joblib 1.5.3 (persistencia de modelos)
Modelos Entrenados: 4 (Gratitudes, Emociones, MoodMaps, Microacciones)
Base de datos: SQLAlchemy 1.4.54 (SQLite/PostgreSQL)
Scheduler: APScheduler 3.10.4
```

---

## 📁 Estructura del Proyecto

```
LUZ/
├── frontend/                # App Flutter
│   ├── lib/screens/        # 3 pantallas principales
│   ├── lib/widgets/        # 7 widgets especializados
│   ├── lib/theme/          # Tema Boho Chic Zen
│   └── assets/             # Avatares y animaciones
│
├── backend/                 # API FastAPI + IA/ML
│   ├── main.py             # Servidor unificado
│   ├── services/           # 5 algoritmos IA
│   ├── models/             # 11 tablas BD
│   └── utils/              # Archivado + limpieza
│
├── datos_demo_luz/          # 🆕 Análisis ML Completo
│   ├── *.csv               # Datos de entrenamiento (4 datasets)
│   ├── analisis_*.ipynb    # 4 notebooks de análisis
│   ├── modelos_entrenados/ # 13 archivos de modelos .pkl
│   │   └── resumen_critico_modelos.ipynb  # Evaluación técnica
│   └── cargar_modelos_completo.py  # Utilidad de carga
```

---

## 🚀 Instalación

### Docker (Recomendado)
```bash
git clone <repository-url> && cd LUZ
docker-compose up --build
# ✅ Backend: http://localhost:8000/docs
```

### Local
```bash
# Backend
cd backend && pip install -r requirements.txt && python main.py

# Frontend
cd frontend && flutter pub get && flutter run
```

**Documentación completa:** http://localhost:8000/docs

---

## 🤖 Sistema de Machine Learning

### Modelos Entrenados Disponibles

El proyecto incluye **4 modelos ML completamente entrenados** con datos sintéticos de demo:

| Modelo | Tipo | Accuracy/Métrica | Estado | Archivo |
|--------|------|------------------|--------|---------|
| **🙏 Gratitudes** | RandomForest | 100% ⚠️ | Overfitting detectado | `modelo_prediccion_gratitudes.pkl` |
| **😤 Emociones** | RandomForest | 40.7% ✅ | Rendimiento realista | `modelo_prediccion_emociones.pkl` |
| **🎭 MoodMaps** | 3x RandomForest | 42.5% ✅ | Multi-dimensional | `modelos_prediccion_moodmaps.pkl` |
| **⚡ Microacciones** | KMeans | 3 clusters ✅ | Exploración válida | `modelo_clustering_microacciones.pkl` |

### Uso del Sistema ML

```python
# Cargar y usar todos los modelos
from datos_demo_luz.cargar_modelos_completo import ModelosLUZ

# Inicializar sistema
modelos = ModelosLUZ()

# Demo completo
modelos.demo_completo()  # Muestra predicciones de todos los modelos

# Uso individual
prediccion_gratitud = modelos.predecir_gratitud(usuario=1, dia=5, hora=20)
cluster_microaccion = modelos.clasificar_microaccion([0.5, -0.3, 0.8, 4.2, 3.8])
```

### Evaluación Crítica

El proyecto incluye un **análisis técnico honesto** en:
- 📊 `datos_demo_luz/modelos_entrenados/resumen_critico_modelos.ipynb`
- 🎯 **Ranking de confiabilidad:** MoodMaps (🥇) > Emociones (🥈) > Microacciones (🥉) > Gratitudes (⚠️)
- 🔍 **Identificación de problemas:** Overfitting en gratitudes, datasets pequeños
- 💡 **Roadmap de mejoras:** Recomendaciones específicas para cada modelo

---

## 🔌 API Endpoints

### Principales
```http
GET  /                     # Info del servidor
GET  /docs                 # Documentación interactiva
POST /moodmap/analizar     # Analizar estado emocional
POST /feedback/enviar      # Enviar feedback
POST /alma/liberar-emocion # Liberar emoción tóxica
GET  /ml/status           # Estado IA/ML
```

### IA/ML
```http
GET  /ml/predict-emotion   # Predicción emocional
GET  /ml/microacciones     # Sugerencias adaptativas
POST /ml/feedback          # Feedback para RL
```

### Testing
```http
POST   /test/crear-usuario   # Crear usuario test
DELETE /test/limpiar         # Limpiar tests
```

**Documentación completa:** http://localhost:8000/docs

---

## 📝 Licencia

Este es un proyecto de prototipo educativo.

---

## 🙏 Agradecimientos

Desarrollado con ❤️ usando:
- **Frontend:** Flutter & Dart
- **Backend:** FastAPI & Python  
- **Machine Learning:** TensorFlow, scikit-learn & pandas
- **Análisis:** Jupyter Notebooks & matplotlib
- **Persistencia:** joblib & pickle

**Estado del proyecto:** ✅ **Completo con 4 modelos ML entrenados y evaluados**

---

## 📞 Contacto

Para preguntas o sugerencias sobre el proyecto Luz.

---

**¡Disfruta de Luz - Tu compañero de bienestar! 🌟✨**
