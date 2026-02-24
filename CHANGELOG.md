# Changelog - Proyecto LUZ

Todos los cambios notables de este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere al [Versionado Semántico](https://semver.org/spec/v2.0.0.html).

## [v1.3.0] - 2026-02-24
### Añadido
- **Sistema de Evaluación Crítica Completa**: Análisis técnico honesto de todos los modelos
- **Notebook de Resumen Crítico**: `resumen_critico_modelos.ipynb` con ranking de confiabilidad
- **Detección de Overfitting**: Identificación automática de métricas sospechosas (gratitudes: 100%)
- **Documentación Académica**: Metodología completa desde problema hasta síntesis
- **EDA Expandido**: Análisis de gratitudes y MoodMaps con perfiles de usuario detallados

### Cambiado
- **Arquitectura Híbrida Consolidada**: RandomForest + KMeans + Sistema de Evaluación
- **README Actualizado**: Métricas reales de los 4 modelos con datos sintéticos clarificados
- **Reorganización**: `resumen_critico_modelos.ipynb` movido a `modelos_entrenados/`
- **Comparativa Técnica**: Análisis detallado vs modelos alternativos (SVM, regresión, etc.)

### Corregido
- **Transparencia en Datos**: Clarificación de que son datos sintéticos, no reales
- **Precisión en Métricas**: Corrección de referencias técnicas en documentación

## [v1.2.0] - 2026-02-10
### Añadido
- **Análisis de MoodMaps**: Dataset de 61 registros con 3 dimensiones emocionales
- **Modelo de Gratitudes**: RandomForest para 23 registros, 14 tipos diferenciados
- **Utilidad de Carga Unificada**: `cargar_modelos_completo.py` con clase ModelosLUZ
- **Demo Completo**: Sistema integrado para probar todos los modelos simultáneamente
- **Correlaciones Inter-dimensionales**: Análisis de felicidad, estrés y motivación

### Cambiado
- **Pipeline ML Completo**: De análisis exploratorio a modelos entrenados guardados
- **Estructura de Metadatos**: Información técnica completa por cada modelo (.pkl)
- **Enfoque Crítico**: Métricas realistas vs accuracy inflado artificialmente

## [v1.1.0] - 2026-01-28
### Añadido
- **Modelo de Emociones Liberadas**: RandomForest, 40.7% accuracy (rendimiento realista)
- **Clustering de Microacciones**: KMeans con 3 clusters identificados
- **13 Archivos de Modelos**: Persistencia completa con joblib y pickle
- **Análisis Exploratorio**: 4 notebooks Jupyter con EDA detallado por dataset
- **Validación Cruzada**: Métricas robustas y detección de patrones temporales

### Cambiado
- **De Mocks a Modelos Reales**: Transición completa de simulaciones a ML entrenado
- **Estructura de Carpetas**: Nueva organización en `datos_demo_luz/`
- **Enfoque de Datos**: Z-score por usuario para eliminar sesgo inter-individual

### Corregido
- **Configuración de Notebooks**: Entorno Python estabilizado para análisis ML
- **Manejo de Datos**: Limpieza y normalización de datasets sintéticos

## [v1.0.0] - 2026-01-11
### Añadido
- **App Flutter Completa**: 3 pantallas principales con tema Boho Chic Zen
  - **MoodMap Board**: Burbujas emocionales animadas interactivas
  - **Alma Board**: Liberación de emociones tóxicas con drag & drop
  - **Destellos de Luz**: Feedback visual personalizable con animaciones
- **Backend FastAPI**: 15+ endpoints con documentación automática
- **Tema Visual Único**: Degradados, sombras y animaciones suaves
- **3 Usuarios Ficticios**: Raquel (meditadora), Carlos (profesional), Lucía (creativa)
- **Natural Chemicals**: Sistema de Serotonina, Dopamina, Endorfinas, Oxitocina
- **Base de Datos**: 11 tablas SQLite auto-creadas con SQLAlchemy
- **Sistema de Archivado**: Datos históricos preservados automáticamente
- **Limpieza Periódica**: Optimización automática mensual programada

### Técnico
- **Stack Tecnológico**: 
  - Frontend: Flutter 3.0+ con Riverpod 2.4.9
  - Backend: FastAPI 0.109.0 con TensorFlow 2.16.1
  - ML: scikit-learn 1.4.0, pandas 2.2.0
  - BD: SQLAlchemy 1.4.54 (SQLite/PostgreSQL)
- **Containerización**: Docker Compose para desarrollo
- **Métricas Iniciales**: 5,700+ líneas de código (2,500 Dart + 3,200 Python)

---

## Tipos de Cambios
- **Añadido** para nuevas funcionalidades.
- **Cambiado** para cambios en funcionalidades existentes.
- **Obsoleto** para funcionalidades que serán eliminadas pronto.
- **Eliminado** para funcionalidades eliminadas.
- **Corregido** para cualquier corrección de errores.
- **Seguridad** en caso de vulnerabilidades.

---

## Nota de Transparencia Académica

Las fechas en este changelog corresponden al desarrollo real del proyecto:
- **Inicio del Proyecto**: 11 enero 2026 (primer commit)
- **Desarrollo ML**: 28 enero - 10 febrero 2026
- **Análisis Crítico**: 24 febrero 2026 (commit actual)

Este timeline refleja 6 semanas de desarrollo autodidacta intensivo, correlacionado con el historial de commits de Git para validación académica.

---

## Enlaces
- [Repositorio](https://github.com/tu-usuario/LUZ) 
- [Documentación](README.md)
- [Issues](https://github.com/tu-usuario/LUZ/issues)

---

**Luz - Tu compañero de bienestar con IA adaptativa** 

Desarrollado con ❤️ usando Flutter, FastAPI, TensorFlow y scikit-learn.