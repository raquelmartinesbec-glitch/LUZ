/// Modelo de usuario ficticio para demostración
class Usuario {
  final int id;
  final String nombre;
  final String avatar;
  final MoodMap moodmap;
  final List<Microaccion> microacciones;
  final AlmaBoard almaBoard;
  final List<Destello> destellos;

  Usuario({
    required this.id,
    required this.nombre,
    required this.avatar,
    required this.moodmap,
    required this.microacciones,
    required this.almaBoard,
    required this.destellos,
  });

  /// Crea un usuario desde JSON
  factory Usuario.fromJson(Map<String, dynamic> json) {
    return Usuario(
      id: json['id'],
      nombre: json['nombre'],
      avatar: json['avatar'],
      moodmap: MoodMap.fromJson(json['moodmap']),
      microacciones: (json['microacciones'] as List)
          .map((m) => Microaccion.fromJson(m))
          .toList(),
      almaBoard: AlmaBoard.fromJson(json['alma_board']),
      destellos: (json['destellos'] as List)
          .map((d) => Destello.fromJson(d))
          .toList(),
    );
  }

  /// Convierte el usuario a JSON
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'nombre': nombre,
      'avatar': avatar,
      'moodmap': moodmap.toJson(),
      'microacciones': microacciones.map((m) => m.toJson()).toList(),
      'alma_board': almaBoard.toJson(),
      'destellos': destellos.map((d) => d.toJson()).toList(),
    };
  }
}

/// Modelo del MoodMap con estados emocionales
class MoodMap {
  final double felicidad;
  final double estres;
  final double motivacion;

  MoodMap({
    required this.felicidad,
    required this.estres,
    required this.motivacion,
  });

  factory MoodMap.fromJson(Map<String, dynamic> json) {
    return MoodMap(
      felicidad: (json['felicidad'] as num).toDouble(),
      estres: (json['estres'] as num).toDouble(),
      motivacion: (json['motivacion'] as num).toDouble(),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'felicidad': felicidad,
      'estres': estres,
      'motivacion': motivacion,
    };
  }

  /// Copia con valores actualizados
  MoodMap copiarCon({
    double? felicidad,
    double? estres,
    double? motivacion,
  }) {
    return MoodMap(
      felicidad: felicidad ?? this.felicidad,
      estres: estres ?? this.estres,
      motivacion: motivacion ?? this.motivacion,
    );
  }
}

/// Modelo de microacción con feedback
class Microaccion {
  final String accion;
  final int feedback;
  final DateTime? fechaEjecucion;

  Microaccion({
    required this.accion,
    required this.feedback,
    this.fechaEjecucion,
  });

  factory Microaccion.fromJson(Map<String, dynamic> json) {
    return Microaccion(
      accion: json['accion'],
      feedback: json['feedback'],
      fechaEjecucion: json['fechaEjecucion'] != null
          ? DateTime.parse(json['fechaEjecucion'])
          : null,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'accion': accion,
      'feedback': feedback,
      'fechaEjecucion': fechaEjecucion?.toIso8601String(),
    };
  }
}

/// Modelo del Alma Board con emociones tóxicas y gratitud
class AlmaBoard {
  final List<String> emocionesToxicasLiberadas;
  final List<String> microaccionesGratitud;

  AlmaBoard({
    required this.emocionesToxicasLiberadas,
    required this.microaccionesGratitud,
  });

  factory AlmaBoard.fromJson(Map<String, dynamic> json) {
    return AlmaBoard(
      emocionesToxicasLiberadas:
          List<String>.from(json['emociones_toxicas_liberadas']),
      microaccionesGratitud:
          List<String>.from(json['microacciones_gratitud']),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'emociones_toxicas_liberadas': emocionesToxicasLiberadas,
      'microacciones_gratitud': microaccionesGratitud,
    };
  }

  /// Agrega una emoción tóxica liberada
  AlmaBoard agregarEmocionToxica(String emocion) {
    return AlmaBoard(
      emocionesToxicasLiberadas: [
        ...emocionesToxicasLiberadas,
        emocion
      ],
      microaccionesGratitud: microaccionesGratitud,
    );
  }

  /// Agrega una microacción de gratitud
  AlmaBoard agregarMicroaccionGratitud(String accion) {
    return AlmaBoard(
      emocionesToxicasLiberadas: emocionesToxicasLiberadas,
      microaccionesGratitud: [...microaccionesGratitud, accion],
    );
  }
}

/// Modelo de destello de luz personalizable
class Destello {
  final String color;
  final String forma;
  final double tamano;
  final double intensidad;

  Destello({
    required this.color,
    required this.forma,
    this.tamano = 1.0,
    this.intensidad = 1.0,
  });

  factory Destello.fromJson(Map<String, dynamic> json) {
    return Destello(
      color: json['color'],
      forma: json['forma'],
      tamano: json['tamano'] != null ? (json['tamano'] as num).toDouble() : 1.0,
      intensidad: json['intensidad'] != null
          ? (json['intensidad'] as num).toDouble()
          : 1.0,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'color': color,
      'forma': forma,
      'tamano': tamano,
      'intensidad': intensidad,
    };
  }
}
