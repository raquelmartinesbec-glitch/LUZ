import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../models/usuario_model.dart';
import '../data/usuarios_ficticios.dart';
import '../services/analisis_emocion_service.dart';
import 'usuario_provider.dart';

/// Provider de análisis emocional con IA
class AnalisisEmocionNotifier extends StateNotifier<AsyncValue<Map<String, dynamic>?>> {
  AnalisisEmocionNotifier() : super(const AsyncValue.data(null));

  /// Analiza el estado emocional con IA y actualiza sugerencias
  Future<void> analizarEstadoEmocional(MoodMap moodmap, int usuarioId) async {
    state = const AsyncValue.loading();
    
    try {
      final resultado = await AnalisisEmocionService.analizarMoodMap(
        felicidad: moodmap.felicidad,
        estres: moodmap.estres,
        motivacion: moodmap.motivacion,
        usuarioId: usuarioId,
      );
      
      state = AsyncValue.data(resultado);
    } catch (e) {
      // En caso de error, generar sugerencias locales
      final sugerenciasLocales = AnalisisEmocionService.generarSugerenciasLocales(
        felicidad: moodmap.felicidad,
        estres: moodmap.estres,
        motivacion: moodmap.motivacion,
      );
      
      state = AsyncValue.data({
        'sugerencias_locales': sugerenciasLocales,
        'modo_offline': true,
        'error': e.toString(),
      });
    }
  }

  /// Procesa el feedback de una actividad completada
  Future<Map<String, double>?> procesarFeedbackActividad({
    required String tipoActividad,
    required String nombreActividad,
    required int intensidad,
    required String? notas,
    required int usuarioId,
    required Map<String, double> estadoAnterior,
  }) async {
    try {
      final resultado = await AnalisisEmocionService.procesarFeedbackActividad(
        tipoActividad: tipoActividad,
        nombreActividad: nombreActividad,
        intensidad: intensidad,
        notas: notas,
        usuarioId: usuarioId,
        estadoAnterior: estadoAnterior,
      );
      
      return {
        'felicidad': resultado['nuevo_estado']['felicidad'],
        'estres': resultado['nuevo_estado']['estres'],
        'motivacion': resultado['nuevo_estado']['motivacion'],
      };
    } catch (e) {
      // Usar cálculo local si falla la conexión
      return AnalisisEmocionService.calcularImpactoActividad(
        tipoChemical: tipoActividad,
        intensidad: intensidad,
        estadoAnterior: estadoAnterior,
      );
    }
  }
}

/// Provider del analizador de emociones con IA
final analisisEmocionProvider = StateNotifierProvider<AnalisisEmocionNotifier, AsyncValue<Map<String, dynamic>?>>((ref) {
  return AnalisisEmocionNotifier();
});

/// Provider mejorado del MoodMap con integración de IA
class MoodMapConIANotifier extends StateNotifier<MoodMap> {
  final Ref ref;

  MoodMapConIANotifier(this.ref) : super(MoodMap(
    felicidad: 0.5,
    estres: 0.5,
    motivacion: 0.5,
  )) {
    // Analizar estado inicial
    _analizarEstadoInicial();
  }

  void _analizarEstadoInicial() async {
    final usuarioActual = ref.read(usuarioActualProvider);
    if (usuarioActual != null) {
      state = usuarioActual.moodmap;
      await _analizarConIA();
    }
  }

  /// Analiza el estado actual con IA
  Future<void> _analizarConIA() async {
    final usuarioActual = ref.read(usuarioActualProvider);
    if (usuarioActual != null) {
      await ref.read(analisisEmocionProvider.notifier)
          .analizarEstadoEmocional(state, usuarioActual.id);
    }
  }

  /// Actualiza el estado emocional tras completar una actividad
  Future<void> actualizarPorActividad({
    required String tipoChemical,
    required String nombreActividad,
    required int intensidad,
    String? notas,
  }) async {
    final usuarioActual = ref.read(usuarioActualProvider);
    if (usuarioActual == null) return;

    final estadoAnterior = {
      'felicidad': state.felicidad,
      'estres': state.estres,
      'motivacion': state.motivacion,
    };

    final nuevoEstado = await ref.read(analisisEmocionProvider.notifier)
        .procesarFeedbackActividad(
      tipoActividad: tipoChemical,
      nombreActividad: nombreActividad,
      intensidad: intensidad,
      notas: notas,
      usuarioId: usuarioActual.id,
      estadoAnterior: estadoAnterior,
    );

    if (nuevoEstado != null) {
      state = MoodMap(
        felicidad: nuevoEstado['felicidad']!,
        estres: nuevoEstado['estres']!,
        motivacion: nuevoEstado['motivacion']!,
      );

      // Re-analizar con el nuevo estado
      await _analizarConIA();
    }
  }

  /// Actualiza manualmente un valor específico
  void actualizarFelicidad(double valor) {
    state = state.copiarCon(felicidad: valor.clamp(0.0, 1.0));
    _analizarConIA();
  }

  void actualizarEstres(double valor) {
    state = state.copiarCon(estres: valor.clamp(0.0, 1.0));
    _analizarConIA();
  }

  void actualizarMotivacion(double valor) {
    state = state.copiarCon(motivacion: valor.clamp(0.0, 1.0));
    _analizarConIA();
  }

  /// Establece un nuevo usuario y analiza su estado
  void establecerUsuario(Usuario usuario) {
    state = usuario.moodmap;
    _analizarConIA();
  }
}

/// Provider del MoodMap con IA
final moodmapConIAProvider = StateNotifierProvider<MoodMapConIANotifier, MoodMap>((ref) {
  return MoodMapConIANotifier(ref);
});

/// Provider para obtener sugerencias de Natural Chemicals
final sugerenciasNaturalChemicalsProvider = Provider<List<String>>((ref) {
  final analisis = ref.watch(analisisEmocionProvider);
  
  return analisis.when(
    data: (data) {
      if (data == null) return [];
      
      if (data.containsKey('sugerencias_locales')) {
        return List<String>.from(data['sugerencias_locales']);
      }
      
      if (data.containsKey('microaccion_sugerida')) {
        // Convertir microacción a natural chemicals
        final microaccion = data['microaccion_sugerida']['microaccion'];
        return _convertirMicroaccionANaturalChemicals(microaccion);
      }
      
      return [];
    },
    loading: () => [],
    error: (error, stack) => ['serotonina'], // Fallback
  );
});

/// Convierte microacciones tradicionales a natural chemicals
List<String> _convertirMicroaccionANaturalChemicals(String microaccion) {
  switch (microaccion.toLowerCase()) {
    case 'calmarse':
      return ['serotonina', 'endorfinas'];
    case 'animarse':
      return ['dopamina', 'serotonina'];
    case 'activarse':
      return ['dopamina', 'endorfinas'];
    case 'conectarse':
      return ['oxitocina'];
    default:
      return ['serotonina'];
  }
}

/// Provider para el estado de conexión con IA
final estadoConexionIAProvider = Provider<bool>((ref) {
  final analisis = ref.watch(analisisEmocionProvider);
  
  return analisis.when(
    data: (data) => data != null && !data.containsKey('modo_offline'),
    loading: () => true,
    error: (error, stack) => false,
  );
});

/// Provider de estadísticas de mejora emocional
final estadisticasMejoraProvider = StateProvider<Map<String, dynamic>>((ref) {
  return {
    'actividades_completadas': 0,
    'mejora_felicidad': 0.0,
    'reduccion_estres': 0.0,
    'aumento_motivacion': 0.0,
    'racha_dias': 0,
    'ultimo_analisis': DateTime.now(),
  };
});