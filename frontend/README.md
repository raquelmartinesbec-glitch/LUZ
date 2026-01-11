# Frontend - Flutter App

## Instalación

### Requisitos
- Flutter SDK 3.0 o superior
- Android Studio / Xcode (para emuladores)
- VS Code (recomendado)

### Pasos

1. **Instalar dependencias:**

```powershell
flutter pub get
```

2. **Verificar dispositivos disponibles:**

```powershell
flutter devices
```

3. **Ejecutar la aplicación:**

```powershell
# En dispositivo conectado o emulador
flutter run

# Para hot reload durante desarrollo
flutter run --hot
```

## Estructura del Proyecto

```
frontend/lib/
├── main.dart                          # Punto de entrada
├── models/
│   └── usuario_model.dart            # Modelos de datos
├── providers/
│   └── usuario_provider.dart         # Gestión de estado (Riverpod)
├── screens/
│   ├── inicio_screen.dart            # Pantalla principal
│   ├── moodmap_screen.dart           # MoodMap Board
│   └── alma_board_screen.dart        # Alma Board
├── widgets/
│   ├── burbuja_emocion.dart          # Burbujas animadas
│   ├── selector_usuario.dart         # Selector de usuario
│   ├── panel_microacciones.dart      # Panel de microacciones
│   ├── feedback_widget.dart          # Feedback post-acción
│   ├── liberacion_emociones_widget.dart  # Liberación de emociones
│   ├── gratitud_widget.dart          # Gratitud y creatividad
│   └── destello_widget.dart          # Destellos de luz
├── theme/
│   └── tema_boho.dart                # Tema visual boho chic zen
└── data/
    └── usuarios_ficticios.dart       # 3 usuarios de demostración
```

## Características Implementadas

### ✅ MoodMap Board
- Burbujas animadas con pulsación
- 3 emociones: Felicidad, Estrés, Motivación
- Tamaño y opacidad según intensidad
- Sombras y efectos de relieve
- Panel de microacciones adaptativas
- Sistema de feedback con sliders

### ✅ Alma Board
- Liberación de emociones con drag & drop
- Campo de texto para emociones personalizadas
- Microacciones de gratitud (grid interactivo)
- Animaciones flotantes
- Resumen de emociones liberadas y gratitudes
- Destellos de luz personalizables

### ✅ Widgets Personalizados
- **BurbujaEmocion**: Visualización con gradientes radiales
- **DestelloWidget**: CustomPainter para formas (estrella, corazón, hoja)
- **FeedbackWidget**: Sliders animados + campo de texto
- **SelectorUsuario**: Dropdown con avatares circulares

### ✅ Animaciones
- AnimationController para pulsaciones
- Transform.scale para efectos de tamaño
- SlideTransition y FadeTransition
- Animaciones flotantes continuas
- Hero transitions (preparadas para navegación)

## Tema Boho Chic Zen

### Colores
```dart
- Color Primario: #D4A59A (Rosa suave)
- Color Secundario: #A8DADC (Azul pastel)
- Color Terciario: #E9C46A (Amarillo suave)
- Fondo: #FAF3F0 (Beige claro)
- Texto: #5D4E4A (Marrón oscuro)
```

### Tipografías
- **Cormorant**: Títulos (display)
- **Montserrat**: Subtítulos y labels
- **Lato**: Texto de cuerpo

### Efectos Visuales
- BoxShadow en todos los elementos
- BorderRadius suaves (15-25px)
- Degradados en fondos y botones
- Sombras difusas para destellos
- Elevation en cards y botones

## Usuarios Ficticios

La app incluye 3 usuarios precargados para demostración:

1. **Raquel Demo**
   - Felicidad: 70% | Estrés: 30% | Motivación: 80%
   - Perfil equilibrado y optimista

2. **Carlos Demo**
   - Felicidad: 50% | Estrés: 60% | Motivación: 40%
   - Perfil desafiante, necesita más apoyo

3. **Lucía Demo**
   - Felicidad: 80% | Estrés: 20% | Motivación: 90%
   - Perfil óptimo, muy motivada

## Navegación

La app usa un sistema de tabs:

- **Tab 1**: MoodMap Board
- **Tab 2**: Alma Board

Selector de usuario en la parte superior para cambiar entre perfiles.

## Próximos Pasos

- [ ] Integrar con backend (HTTP requests con Dio)
- [ ] Implementar SQLite para persistencia local
- [ ] Agregar Hero animations entre pantallas
- [ ] Implementar notificaciones locales
- [ ] Agregar modo oscuro
- [ ] Tests unitarios y de widgets

## Comandos Útiles

```powershell
# Limpiar build
flutter clean

# Actualizar dependencias
flutter pub upgrade

# Analizar código
flutter analyze

# Ejecutar tests
flutter test

# Generar APK
flutter build apk

# Generar iOS
flutter build ios
```

## Notas de Desarrollo

- Usar `flutter run --hot` para hot reload
- Los cambios en pubspec.yaml requieren `flutter pub get`
- Para cambios en assets, hacer full restart
- Revisar logs con `flutter logs`
