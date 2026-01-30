import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../theme/tema_boho.dart';
import '../providers/usuario_provider.dart';
import '../widgets/burbuja_emocion.dart';
import '../widgets/panel_microacciones.dart';
import '../widgets/feedback_widget.dart';
import 'dart:math' as math;

/// Pantalla del MoodMap Board
/// Visualiza emociones en burbujas animadas con sombras y relieve
class MoodMapScreen extends ConsumerStatefulWidget {
  const MoodMapScreen({super.key});

  @override
  ConsumerState<MoodMapScreen> createState() => _MoodMapScreenState();
}

class _MoodMapScreenState extends ConsumerState<MoodMapScreen>
    with TickerProviderStateMixin {
  late AnimationController _animationController;
  late Animation<double> _pulseAnimation;
  bool _mostrarFeedback = false;
  String? _microaccionSeleccionada;

  @override
  void initState() {
    super.initState();
    
    // Animación de pulsación para las burbujas
    _animationController = AnimationController(
      duration: const Duration(milliseconds: 2000),
      vsync: this,
    )..repeat(reverse: true);

    _pulseAnimation = Tween<double>(begin: 0.95, end: 1.05).animate(
      CurvedAnimation(
        parent: _animationController,
        curve: Curves.easeInOut,
      ),
    );
  }

  @override
  void dispose() {
    _animationController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final moodmap = ref.watch(moodmapProvider);

    if (moodmap == null) {
      return const Center(
        child: Text('Selecciona un usuario para ver su MoodMap'),
      );
    }

    return SingleChildScrollView(
      padding: const EdgeInsets.all(20),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Título de la sección
          Text(
            '¿Cómo te sientes?',
            style: Theme.of(context).textTheme.headlineMedium,
          ),
          const SizedBox(height: 8),
          Text(
            'Visualiza tus emociones en tiempo real',
            style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                  color: TemaBoho.colorTexto.withOpacity(0.7),
                ),
          ),
          const SizedBox(height: 30),

          // Burbujas de emociones
          _construirBurbujasEmociones(moodmap),

          const SizedBox(height: 40),

          // Panel de microacciones adaptativas
          if (!_mostrarFeedback) ...[
            Text(
              'Microacciones para ti',
              style: Theme.of(context).textTheme.titleLarge,
            ),
            const SizedBox(height: 16),
            PanelMicroacciones(
              onMicroaccionSeleccionada: (accion) {
                setState(() {
                  _microaccionSeleccionada = accion;
                  _mostrarFeedback = true;
                });
              },
            ),
          ],

          // Widget de feedback post-acción
          if (_mostrarFeedback && _microaccionSeleccionada != null) ...[
            const SizedBox(height: 20),
            FeedbackWidget(
              microaccion: _microaccionSeleccionada!,
              onFeedbackEnviado: () {
                setState(() {
                  _mostrarFeedback = false;
                  _microaccionSeleccionada = null;
                });
                
                // Mostrar mensaje de confirmación
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(
                    content: const Text('¡Gracias por tu feedback! 💫'),
                    backgroundColor: TemaBoho.colorPrimario,
                    behavior: SnackBarBehavior.floating,
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(10),
                    ),
                  ),
                );
              },
            ),
          ],
        ],
      ),
    );
  }

  /// Construye las burbujas de emociones con animaciones
  Widget _construirBurbujasEmociones(dynamic moodmap) {
    return Container(
      height: 300,
      decoration: BoxDecoration(
        color: Colors.white.withOpacity(0.5),
        borderRadius: BorderRadius.circular(30),
        boxShadow: TemaBoho.obtenerSombraRelieve(),
      ),
      child: Stack(
        children: [
          // Burbuja de Felicidad
          Positioned(
            left: 40,
            top: 50,
            child: AnimatedBuilder(
              animation: _pulseAnimation,
              builder: (context, child) {
                return Transform.scale(
                  scale: _pulseAnimation.value,
                  child: BurbujaEmocion(
                    emocion: 'Felicidad',
                    valor: moodmap.felicidad,
                    color: TemaBoho.colorFelicidad,
                    icono: Icons.sentiment_very_satisfied,
                  ),
                );
              },
            ),
          ),

          // Burbuja de Estrés
          Positioned(
            right: 50,
            top: 80,
            child: AnimatedBuilder(
              animation: _pulseAnimation,
              builder: (context, child) {
                return Transform.scale(
                  scale: 2.0 - _pulseAnimation.value, // Efecto inverso
                  child: BurbujaEmocion(
                    emocion: 'Estrés',
                    valor: moodmap.estres,
                    color: TemaBoho.colorEstres,
                    icono: Icons.psychology_alt,
                  ),
                );
              },
            ),
          ),

          // Burbuja de Motivación
          Positioned(
            left: MediaQuery.of(context).size.width * 0.35,
            bottom: 40,
            child: AnimatedBuilder(
              animation: _pulseAnimation,
              builder: (context, child) {
                return Transform.scale(
                  scale: _pulseAnimation.value,
                  child: BurbujaEmocion(
                    emocion: 'Motivación',
                    valor: moodmap.motivacion,
                    color: TemaBoho.colorMotivacion,
                    icono: Icons.rocket_launch,
                  ),
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}
