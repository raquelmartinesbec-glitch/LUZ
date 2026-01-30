import '../models/usuario_model.dart';

/// Lista de usuarios ficticios para demostración
/// Datos precargados según especificaciones del proyecto
final List<Usuario> usuariosFicticios = [
  // Usuario 1: Raquel Demo
  Usuario(
    id: 1,
    nombre: "Raquel Demo",
    avatar: "avatar1.png",
    moodmap: MoodMap(
      felicidad: 0.7,
      estres: 0.3,
      motivacion: 0.8,
    ),
    microacciones: [
      Microaccion(
        accion: "calmarse",
        feedback: 4,
        fechaEjecucion: DateTime.now().subtract(const Duration(hours: 2)),
      ),
      Microaccion(
        accion: "animarse",
        feedback: 3,
        fechaEjecucion: DateTime.now().subtract(const Duration(hours: 5)),
      ),
    ],
    almaBoard: AlmaBoard(
      emocionesToxicasLiberadas: ["frustración", "preocupación"],
      microaccionesGratitud: [
        "escribir 3 cosas por las que estoy agradecida"
      ],
    ),
    destellos: [
      Destello(
        color: "amarillo",
        forma: "estrella",
        tamano: 1.2,
        intensidad: 0.9,
      ),
    ],
  ),

  // Usuario 2: Carlos Demo
  Usuario(
    id: 2,
    nombre: "Carlos Demo",
    avatar: "avatar2.png",
    moodmap: MoodMap(
      felicidad: 0.5,
      estres: 0.6,
      motivacion: 0.4,
    ),
    microacciones: [
      Microaccion(
        accion: "activarse",
        feedback: 5,
        fechaEjecucion: DateTime.now().subtract(const Duration(hours: 1)),
      ),
      Microaccion(
        accion: "calmarse",
        feedback: 3,
        fechaEjecucion: DateTime.now().subtract(const Duration(hours: 3)),
      ),
    ],
    almaBoard: AlmaBoard(
      emocionesToxicasLiberadas: ["ansiedad", "miedo"],
      microaccionesGratitud: ["dibujar una idea creativa"],
    ),
    destellos: [
      Destello(
        color: "verde",
        forma: "hoja",
        tamano: 1.0,
        intensidad: 0.8,
      ),
    ],
  ),

  // Usuario 3: Lucía Demo
  Usuario(
    id: 3,
    nombre: "Lucía Demo",
    avatar: "avatar3.png",
    moodmap: MoodMap(
      felicidad: 0.8,
      estres: 0.2,
      motivacion: 0.9,
    ),
    microacciones: [
      Microaccion(
        accion: "animarse",
        feedback: 5,
        fechaEjecucion: DateTime.now().subtract(const Duration(minutes: 30)),
      ),
      Microaccion(
        accion: "activarse",
        feedback: 4,
        fechaEjecucion: DateTime.now().subtract(const Duration(hours: 4)),
      ),
    ],
    almaBoard: AlmaBoard(
      emocionesToxicasLiberadas: ["tristeza", "preocupación"],
      microaccionesGratitud: [
        "meditación guiada",
        "escribir afirmaciones positivas"
      ],
    ),
    destellos: [
      Destello(
        color: "rosa",
        forma: "corazon",
        tamano: 1.5,
        intensidad: 1.0,
      ),
    ],
  ),
];
