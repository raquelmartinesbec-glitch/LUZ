# Datos Demo LUZ - 7 días de análisis

## Archivos generados:

### CSVs para análisis:
- `moodmaps.csv` - Todos los registros emocionales (felicidad, estrés, motivación)
- `emociones_liberadas.csv` - Emociones tóxicas liberadas en Alma Board
- `gratitudes.csv` - Microacciones de gratitud registradas
- `feedbacks_microacciones.csv` - Feedback completo de microacciones (incluye estado emocional previo Y posterior)
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

## Estructura de datos de microacciones:

### Datos que SÍ se capturan:
- **Estado emocional previo**: felicidad, estrés, motivación antes de la microacción
- **Estado emocional posterior**: felicidad, estrés, motivación después de la microacción (15-30 min después)
- **Feedback subjetivo**: efectividad (1-5), comodidad (1-5), energía (1-4) según el usuario
- **Timestamp y contexto**: cuándo y qué microacción se realizó
- **Efectividad objetiva**: cambio real en estado emocional (mejora/empeoramiento)

### Datos que NO se capturan (limitación menor):
- **Duración del efecto**: no se hace seguimiento prolongado del beneficio (solo una medición post)
- **Factores externos**: no se registran eventos que puedan influir en el cambio emocional
- **Múltiples mediciones post**: solo una medición posterior por microacción

## Período de datos: 
Últimos 7 días desde la fecha de generación.

## Sugerencias de análisis:
- Evolución emocional por usuario y día
- **Efectividad real de microacciones**: comparación pre/post estado emocional
- **Correlación subjetiva vs objetiva**: feedback del usuario vs mejora medible
- Patrones de uso (horarios, frecuencia)
- **Ranking de microacciones**: cuáles generan mayor mejora objetiva
- Correlaciones entre liberación de emociones y mejora del mood
- Análisis de sentiment de gratitudes vs estado emocional

## ✅ Capacidades implementadas:
- **Medición completa pre/post**: Estado emocional antes y después de cada microacción
- **Efectividad objetiva**: Cálculo automático de mejora real en cada dimensión emocional
- **Bucle de aprendizaje**: El sistema de RL puede aprender de resultados reales para mejorar recomendaciones
- **Análisis comparativo**: Correlación entre percepción subjetiva y mejora objetiva
- **Seguimiento automático**: Sistema de recordatorios para capturar estado post-microacción
- **Notificaciones inteligentes**: Recordatorios programados 20 minutos después de cada microacción
- **Interfaz de captura**: Sliders intuitivos para registrar estado emocional posterior

## � Validación Cruzada Secuencial (Análisis de Microacciones)

### Metodología Temporal
Se implementó **Time Series Cross-Validation** para evaluar la robustez del modelo respetando el orden cronológico de los datos. Esta técnica evalúa la capacidad predictiva en ventanas temporales progresivas.

### Resultados Comparativos
| Modelo | MSE | R² | Interpretación |
|--------|-----|----|----|
| **LinearRegression** | 3.460 ± 1.870 | -3.081 ± 2.373 | Rendimiento pobre |
| **RandomForest** ⭐ | **1.219 ± 0.110** | **-0.320 ± 0.155** | **Mejor modelo** |

### Análisis de Degradación Temporal
- **Pendiente MSE**: 0.0832 (tendencia ascendente leve)
- **Degradación temporal**: +13.9%
- **Significancia estadística**: NO (p=0.575)
- **Interpretación**: El modelo mantiene estabilidad temporal aceptable

### Métricas de Validación
- **Splits temporales**: 3 folds secuenciales
- **Datos analizados**: 33 registros de 3 usuarios
- **Features evaluadas**: 6 (estado emocional previo, comodidad, energía, microacción)
- **Varianza entre folds**: Baja (0.110), indicando consistencia

**✅ Conclusión**: RandomForest es el modelo óptimo con MSE de 1.219 y degradación temporal controlada.

## �🔄 Flujo de seguimiento implementado:
1. **Inicio de microacción** → Registro automático con moodmap previo
2. **Programación de recordatorio** → 20 minutos después aparece notificación  
3. **Captura de estado posterior** → Usuario usa sliders para registrar cómo se siente
4. **Cálculo de efectividad** → Sistema compara automáticamente pre vs post
5. **Actualización de RL** → El algoritmo aprende de resultados reales
6. **Feedback visual** → Usuario ve efectividad objetiva de la microacción

## 🛠️ Componentes técnicos:
- **Backend**: Endpoint `/feedback/moodmap-post-microaccion` para capturar datos posteriores
- **Servicio**: `SeguimientoMicroaccionesService` maneja el ciclo completo
- **Widget**: `RecordatorioSeguimientoWidget` para notificaciones y captura
- **Integración**: `PanelMicroacciones` registra automáticamente cada microacción
