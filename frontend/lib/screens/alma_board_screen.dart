import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../theme/tema_boho.dart';
import '../providers/usuario_provider.dart';
import '../widgets/liberacion_emociones_widget.dart';
import '../widgets/gratitud_widget.dart';
import '../widgets/destello_widget.dart';

/// Pantalla del Alma Board
/// Liberación de emociones tóxicas y microacciones de gratitud/creatividad
class AlmaBoardScreen extends ConsumerStatefulWidget {
  const AlmaBoardScreen({super.key});

  @override
  ConsumerState<AlmaBoardScreen> createState() => _AlmaBoardScreenState();
}

class _AlmaBoardScreenState extends ConsumerState<AlmaBoardScreen>
    with TickerProviderStateMixin {
  late AnimationController _floatController;
  late Animation<double> _floatAnimation;

  @override
  void initState() {
    super.initState();

    // Animación flotante para los elementos
    _floatController = AnimationController(
      duration: const Duration(milliseconds: 3000),
      vsync: this,
    )..repeat(reverse: true);

    _floatAnimation = Tween<double>(begin: -10, end: 10).animate(
      CurvedAnimation(
        parent: _floatController,
        curve: Curves.easeInOut,
      ),
    );
  }

  @override
  void dispose() {
    _floatController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final almaBoard = ref.watch(almaBoardProvider);
    final destellos = ref.watch(destellosProvider);

    if (almaBoard == null) {
      return const Center(
        child: Text('Selecciona un usuario para ver su Alma Board'),
      );
    }

    return Stack(
      children: [
        SingleChildScrollView(
          padding: const EdgeInsets.all(20),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Título con animación
              AnimatedBuilder(
                animation: _floatAnimation,
                builder: (context, child) {
                  return Transform.translate(
                    offset: Offset(0, _floatAnimation.value),
                    child: child,
                  );
                },
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Alma Board',
                      style: Theme.of(context).textTheme.headlineMedium,
                    ),
                    const SizedBox(height: 8),
                    Text(
                      'Libera, agradece y crea',
                      style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                            color: TemaBoho.colorTexto.withOpacity(0.7),
                          ),
                    ),
                  ],
                ),
              ),

              const SizedBox(height: 30),

              // Sección de liberación de emociones tóxicas
              _construirSeccion(
                titulo: '🌊 Libera tus emociones',
                descripcion: 'Arrastra y suelta lo que no necesitas',
                child: LiberacionEmocionesWidget(
                  emocionesLiberadas: almaBoard.emocionesToxicasLiberadas,
                  onEmocionLiberada: (emocion) {
                    ref
                        .read(almaBoardNotifierProvider.notifier)
                        .liberarEmocionToxica(emocion);
                    _mostrarDestello();
                  },
                ),
              ),

              const SizedBox(height: 30),

              // Sección de gratitud y creatividad
              _construirSeccion(
                titulo: '✨ Cultiva gratitud',
                descripcion: 'Escribe, dibuja, agradece',
                child: GratitudWidget(
                  microaccionesGratitud: almaBoard.microaccionesGratitud,
                  onGratitudAgregada: (accion) {
                    ref
                        .read(almaBoardNotifierProvider.notifier)
                        .agregarGratitud(accion);
                    _mostrarDestello();
                  },
                ),
              ),

              const SizedBox(height: 30),

              // Resumen de emociones liberadas
              if (almaBoard.emocionesToxicasLiberadas.isNotEmpty)
                _construirResumen(
                  'Emociones liberadas',
                  almaBoard.emocionesToxicasLiberadas,
                  TemaBoho.colorEstres,
                ),

              const SizedBox(height: 20),

              // Resumen de gratitudes
              if (almaBoard.microaccionesGratitud.isNotEmpty)
                _construirResumen(
                  'Momentos de gratitud',
                  almaBoard.microaccionesGratitud,
                  TemaBoho.colorMotivacion,
                ),

              const SizedBox(height: 100), // Espacio para los destellos
            ],
          ),
        ),

        // Destellos de luz flotantes
        if (destellos.isNotEmpty)
          ...destellos.asMap().entries.map((entry) {
            return DestelloWidget(
              destello: entry.value,
              posicion: Offset(
                50.0 + (entry.key * 60.0),
                MediaQuery.of(context).size.height - 150,
              ),
            );
          }),
      ],
    );
  }

  /// Construye una sección con título y descripción
  Widget _construirSeccion({
    required String titulo,
    required String descripcion,
    required Widget child,
  }) {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: Colors.white.withOpacity(0.8),
        borderRadius: BorderRadius.circular(25),
        boxShadow: TemaBoho.obtenerSombraRelieve(),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            titulo,
            style: Theme.of(context).textTheme.titleLarge,
          ),
          const SizedBox(height: 4),
          Text(
            descripcion,
            style: Theme.of(context).textTheme.bodySmall?.copyWith(
                  color: TemaBoho.colorTexto.withOpacity(0.6),
                ),
          ),
          const SizedBox(height: 20),
          child,
        ],
      ),
    );
  }

  /// Construye el resumen de emociones/gratitudes
  Widget _construirResumen(String titulo, List<String> items, Color color) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        gradient: LinearGradient(
          colors: [
            color.withOpacity(0.2),
            color.withOpacity(0.05),
          ],
        ),
        borderRadius: BorderRadius.circular(20),
        border: Border.all(
          color: color.withOpacity(0.3),
          width: 1,
        ),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            titulo,
            style: Theme.of(context).textTheme.titleMedium?.copyWith(
                  color: color,
                  fontWeight: FontWeight.w600,
                ),
          ),
          const SizedBox(height: 12),
          Wrap(
            spacing: 8,
            runSpacing: 8,
            children: items
                .map(
                  (item) => Container(
                    padding:
                        const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                    decoration: BoxDecoration(
                      color: Colors.white,
                      borderRadius: BorderRadius.circular(15),
                      boxShadow: [
                        BoxShadow(
                          color: color.withOpacity(0.2),
                          blurRadius: 4,
                          offset: const Offset(0, 2),
                        ),
                      ],
                    ),
                    child: Text(
                      item,
                      style: Theme.of(context).textTheme.bodySmall?.copyWith(
                            color: color,
                          ),
                    ),
                  ),
                )
                .toList(),
          ),
        ],
      ),
    );
  }

  /// Muestra un destello de luz al completar una acción
  void _mostrarDestello() {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: const Row(
          children: [
            Icon(Icons.auto_awesome, color: Colors.white),
            SizedBox(width: 8),
            Text('¡Destello de luz activado! ✨'),
          ],
        ),
        backgroundColor: TemaBoho.colorTerciario,
        behavior: SnackBarBehavior.floating,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(10),
        ),
        duration: const Duration(seconds: 2),
      ),
    );
  }
}
