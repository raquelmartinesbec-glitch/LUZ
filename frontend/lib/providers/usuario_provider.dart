import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../models/usuario_model.dart';
import '../data/usuarios_ficticios.dart';

/// Provider del usuario actual seleccionado
final usuarioActualProvider = StateProvider<Usuario?>((ref) {
  // Por defecto, selecciona el primer usuario ficticio
  return usuariosFicticios.isNotEmpty ? usuariosFicticios[0] : null;
});

/// Provider de la lista de todos los usuarios ficticios
final usuariosListaProvider = Provider<List<Usuario>>((ref) {
  return usuariosFicticios;
});

/// Provider del MoodMap del usuario actual
final moodmapProvider = StateProvider<MoodMap?>((ref) {
  final usuario = ref.watch(usuarioActualProvider);
  return usuario?.moodmap;
});

/// Provider del Alma Board del usuario actual
final almaBoardProvider = StateProvider<AlmaBoard?>((ref) {
  final usuario = ref.watch(usuarioActualProvider);
  return usuario?.almaBoard;
});

/// Provider de las microacciones del usuario actual
final microaccionesProvider = StateProvider<List<Microaccion>>((ref) {
  final usuario = ref.watch(usuarioActualProvider);
  return usuario?.microacciones ?? [];
});

/// Provider de los destellos del usuario actual
final destellosProvider = StateProvider<List<Destello>>((ref) {
  final usuario = ref.watch(usuarioActualProvider);
  return usuario?.destellos ?? [];
});

/// Notifier para gestionar actualizaciones del MoodMap
class MoodMapNotifier extends StateNotifier<MoodMap> {
  MoodMapNotifier()
      : super(MoodMap(
          felicidad: 0.5,
          estres: 0.5,
          motivacion: 0.5,
        ));

  /// Actualiza el nivel de felicidad (0.0 - 1.0)
  void actualizarFelicidad(double valor) {
    state = state.copiarCon(felicidad: valor.clamp(0.0, 1.0));
  }

  /// Actualiza el nivel de estrés (0.0 - 1.0)
  void actualizarEstres(double valor) {
    state = state.copiarCon(estres: valor.clamp(0.0, 1.0));
  }

  /// Actualiza el nivel de motivación (0.0 - 1.0)
  void actualizarMotivacion(double valor) {
    state = state.copiarCon(motivacion: valor.clamp(0.0, 1.0));
  }

  /// Actualiza todos los valores del MoodMap
  void actualizarTodo({
    required double felicidad,
    required double estres,
    required double motivacion,
  }) {
    state = MoodMap(
      felicidad: felicidad.clamp(0.0, 1.0),
      estres: estres.clamp(0.0, 1.0),
      motivacion: motivacion.clamp(0.0, 1.0),
    );
  }
}

/// Provider del MoodMap Notifier
final moodmapNotifierProvider =
    StateNotifierProvider<MoodMapNotifier, MoodMap>((ref) {
  return MoodMapNotifier();
});

/// Notifier para gestionar el Alma Board
class AlmaBoardNotifier extends StateNotifier<AlmaBoard> {
  AlmaBoardNotifier()
      : super(AlmaBoard(
          emocionesToxicasLiberadas: ['Ansiedad por el trabajo'],
          microaccionesGratitud: [
            'Estoy agradecido/a por mi familia que siempre me apoya',
            'Agradezco tener salud',
            'Me siento afortunado/a por poder aprender cosas nuevas cada día'
          ],
        ));

  /// Libera una emoción tóxica
  void liberarEmocionToxica(String emocion) {
    state = state.agregarEmocionToxica(emocion);
  }

  /// Agrega una microacción de gratitud
  void agregarGratitud(String accion) {
    state = state.agregarMicroaccionGratitud(accion);
  }

  /// Reinicia el Alma Board
  void reiniciar() {
    state = AlmaBoard(
      emocionesToxicasLiberadas: [],
      microaccionesGratitud: [],
    );
  }
}

/// Provider del Alma Board Notifier
final almaBoardNotifierProvider =
    StateNotifierProvider<AlmaBoardNotifier, AlmaBoard>((ref) {
  return AlmaBoardNotifier();
});
