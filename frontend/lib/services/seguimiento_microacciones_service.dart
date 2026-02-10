import 'package:flutter/material.dart';
import '../models/usuario_model.dart';

/// Servicio para manejo de seguimiento post-microacción
/// Programa recordatorios y captura moodmaps posteriores
class SeguimientoMicroaccionesService {
  static final SeguimientoMicroaccionesService _instance = 
      SeguimientoMicroaccionesService._internal();
  
  factory SeguimientoMicroaccionesService() => _instance;
  SeguimientoMicroaccionesService._internal();

  // Microacciones pendientes de seguimiento
  final Map<String, MicroaccionPendiente> _microaccionesPendientes = {};

  /// Registra una microacción para seguimiento posterior
  void registrarMicroaccion({
    required String usuarioId,
    required String tipoMicroaccion,
    required MoodMap moodmapPrevio,
    int minutosEspera = 20,
  }) {
    final id = '${usuarioId}_${tipoMicroaccion}_${DateTime.now().millisecondsSinceEpoch}';
    
    _microaccionesPendientes[id] = MicroaccionPendiente(
      id: id,
      usuarioId: usuarioId,
      tipoMicroaccion: tipoMicroaccion,
      moodmapPrevio: moodmapPrevio,
      momentoInicio: DateTime.now(),
      momentoRecordatorio: DateTime.now().add(Duration(minutes: minutosEspera)),
    );

    // Programar notificación (si está disponible)
    _programarRecordatorio(id, minutosEspera);

    debugPrint('🔔 Microacción registrada para seguimiento: $tipoMicroaccion');
  }

  /// Captura el moodmap posterior y completa el seguimiento
  Future<Map<String, dynamic>> completarSeguimiento({
    required String usuarioId,
    required String tipoMicroaccion,
    required MoodMap moodmapPosterior,
  }) async {
    // Buscar microacción pendiente
    final pendiente = _microaccionesPendientes.values
        .where((m) => m.usuarioId == usuarioId && 
                      m.tipoMicroaccion == tipoMicroaccion &&
                      !m.completada)
        .firstOrNull;

    if (pendiente == null) {
      throw Exception('No se encontró microacción pendiente para $tipoMicroaccion');
    }

    // Marcar como completada
    pendiente.completada = true;
    pendiente.moodmapPosterior = moodmapPosterior;
    pendiente.momentoCompletado = DateTime.now();

    // Calcular efectividad
    final efectividad = _calcularEfectividad(
      pendiente.moodmapPrevio, 
      moodmapPosterior,
    );

    // Enviar al backend
    try {
      final resultado = await _enviarAlBackend(pendiente, efectividad);
      
      // Limpiar de pendientes
      _microaccionesPendientes.remove(pendiente.id);
      
      return {
        'exito': true,
        'efectividad_objetiva': efectividad['total'],
        'mejoras': efectividad['desglose'],
        'mensaje': resultado['mensaje'],
      };
      
    } catch (e) {
      debugPrint('❌ Error enviando seguimiento al backend: $e');
      // No eliminamos de pendientes para reintento
      return {
        'exito': false,
        'error': e.toString(),
      };
    }
  }

  /// Obtiene microacciones pendientes de un usuario
  List<MicroaccionPendiente> obtenerPendientes(String usuarioId) {
    return _microaccionesPendientes.values
        .where((m) => m.usuarioId == usuarioId && !m.completada)
        .toList()
        ..sort((a, b) => a.momentoRecordatorio.compareTo(b.momentoRecordatorio));
  }

  /// Verifica si hay recordatorios pendientes
  List<MicroaccionPendiente> obtenerRecordatoriosPendientes() {
    final ahora = DateTime.now();
    return _microaccionesPendientes.values
        .where((m) => !m.completada && 
                      !m.recordatorioMostrado &&
                      ahora.isAfter(m.momentoRecordatorio))
        .toList();
  }

  /// Marca un recordatorio como mostrado
  void marcarRecordatorioMostrado(String microaccionId) {
    final microaccion = _microaccionesPendientes[microaccionId];
    if (microaccion != null) {
      microaccion.recordatorioMostrado = true;
    }
  }

  /// Calcula la efectividad objetiva comparando moodmaps
  Map<String, dynamic> _calcularEfectividad(
    MoodMap previo,
    MoodMap posterior,
  ) {
    final mejorFelicidad = posterior.felicidad - previo.felicidad;
    final mejorEstres = previo.estres - posterior.estres; // Reducción es positiva
    final mejorMotivacion = posterior.motivacion - previo.motivacion;
    
    final efectividadTotal = (mejorFelicidad + mejorEstres + mejorMotivacion) / 3;

    return {
      'total': efectividadTotal,
      'desglose': {
        'felicidad': mejorFelicidad,
        'estres': mejorEstres,
        'motivacion': mejorMotivacion,
      },
    };
  }

  /// Envía los datos al backend
  Future<Map<String, dynamic>> _enviarAlBackend(
    MicroaccionPendiente pendiente,
    Map<String, dynamic> efectividad,
  ) async {
    // Simular llamada HTTP (reemplazar con http real)
    await Future.delayed(Duration(milliseconds: 500));
    
    // Datos a enviar
    final datos = {
      'usuario_id': pendiente.usuarioId,
      'microaccion': pendiente.tipoMicroaccion,
      'moodmap_posterior': {
        'felicidad': pendiente.moodmapPosterior!.felicidad,
        'estres': pendiente.moodmapPosterior!.estres,
        'motivacion': pendiente.moodmapPosterior!.motivacion,
      },
      'timestamp_inicio': pendiente.momentoInicio.toIso8601String(),
      'timestamp_completado': pendiente.momentoCompletado!.toIso8601String(),
    };

    debugPrint('📤 Enviando seguimiento al backend: $datos');

    // TODO: Implementar llamada HTTP real a /feedback/moodmap-post-microaccion
    // final response = await http.post(
    //   Uri.parse('$BASE_URL/feedback/moodmap-post-microaccion'),
    //   headers: {'Content-Type': 'application/json'},
    //   body: json.encode(datos),
    // );

    return {
      'mensaje': 'Seguimiento registrado exitosamente',
      'efectividad_objetiva': efectividad['total'],
    };
  }

  /// Programa recordatorio (placeholder para notificaciones)
  void _programarRecordatorio(String microaccionId, int minutos) {
    // TODO: Integrar con sistema de notificaciones locales
    debugPrint('⏰ Recordatorio programado en $minutos minutos para $microaccionId');
  }

  /// Limpia microacciones completadas antiguas
  void limpiarCompletadas() {
    final hace24Horas = DateTime.now().subtract(Duration(hours: 24));
    
    _microaccionesPendientes.removeWhere((key, microaccion) =>
        microaccion.completada &&
        microaccion.momentoCompletado != null &&
        microaccion.momentoCompletado!.isBefore(hace24Horas));
  }
}

/// Modelo para microacción pendiente de seguimiento
class MicroaccionPendiente {
  final String id;
  final String usuarioId;
  final String tipoMicroaccion;
  final MoodMap moodmapPrevio;
  final DateTime momentoInicio;
  final DateTime momentoRecordatorio;
  
  MoodMap? moodmapPosterior;
  DateTime? momentoCompletado;
  bool completada;
  bool recordatorioMostrado;

  MicroaccionPendiente({
    required this.id,
    required this.usuarioId,
    required this.tipoMicroaccion,
    required this.moodmapPrevio,
    required this.momentoInicio,
    required this.momentoRecordatorio,
    this.moodmapPosterior,
    this.momentoCompletado,
    this.completada = false,
    this.recordatorioMostrado = false,
  });

  /// Tiempo transcurrido desde el inicio
  Duration get tiempoTranscurrido => DateTime.now().difference(momentoInicio);
  
  /// Tiempo hasta el recordatorio (o desde el recordatorio si ya pasó)
  Duration get tiempoHastaRecordatorio => momentoRecordatorio.difference(DateTime.now());
  
  /// Si ya es momento de mostrar el recordatorio
  bool get esHoraDeRecordatorio => DateTime.now().isAfter(momentoRecordatorio);

  @override
  String toString() => 'MicroaccionPendiente($tipoMicroaccion, completada: $completada)';
}