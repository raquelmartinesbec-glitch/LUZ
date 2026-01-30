import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../theme/tema_boho.dart';
import '../providers/usuario_provider.dart';
import '../providers/analisis_ia_provider.dart';
import '../widgets/burbuja_emocion.dart';
import '../widgets/panel_natural_chemicals.dart';
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
  Map<String, dynamic>? _naturalChemicalSeleccionado;

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
    final moodmap = ref.watch(moodmapConIAProvider);
    final analisisIA = ref.watch(analisisEmocionProvider);
    final sugerenciasIA = ref.watch(sugerenciasNaturalChemicalsProvider);
    final conexionIA = ref.watch(estadoConexionIAProvider);
    final usuarioActual = ref.watch(usuarioActualProvider);

    if (usuarioActual == null) {
      return const Center(
        child: Text('Selecciona un usuario para ver su MoodMap'),
      );
    }

    return SingleChildScrollView(
      padding: const EdgeInsets.all(20),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Título de la sección con indicador de IA
          Row(
            children: [
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      '¿Cómo te sientes?',
                      style: Theme.of(context).textTheme.headlineMedium,
                    ),
                    const SizedBox(height: 4),
                    Text(
                      'Análisis emocional con IA • Tiempo real',
                      style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                            color: TemaBoho.colorTexto.withOpacity(0.7),
                          ),
                    ),
                  ],
                ),
              ),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                decoration: BoxDecoration(
                  color: conexionIA ? Colors.green : Colors.orange,
                  borderRadius: BorderRadius.circular(20),
                ),
                child: Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Icon(
                      conexionIA ? Icons.psychology : Icons.offline_bolt,
                      size: 16,
                      color: Colors.white,
                    ),
                    const SizedBox(width: 4),
                    Text(
                      conexionIA ? 'IA Online' : 'Modo Local',
                      style: const TextStyle(
                        color: Colors.white,
                        fontSize: 12,
                        fontWeight: FontWeight.w600,
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
          const SizedBox(height: 30),

          // Burbujas de emociones
          _construirBurbujasEmociones(moodmap),

          const SizedBox(height: 40),

          // Panel de Natural Chemicals con IA
          if (!_mostrarFeedback) ...[
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  children: [
                    Expanded(
                      child: Text(
                        'Natural Chemicals para ti',
                        style: Theme.of(context).textTheme.titleLarge,
                      ),
                    ),
                    if (analisisIA.isLoading)
                      const SizedBox(
                        width: 20,
                        height: 20,
                        child: CircularProgressIndicator(strokeWidth: 2),
                      ),
                  ],
                ),
                
                // Sugerencias de IA
                if (sugerenciasIA.isNotEmpty) ...[
                  const SizedBox(height: 8),
                  Container(
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: TemaBoho.colorPrimario.withOpacity(0.1),
                      borderRadius: BorderRadius.circular(15),
                      border: Border.all(
                        color: TemaBoho.colorPrimario.withOpacity(0.3),
                      ),
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          children: [
                            Icon(
                              Icons.psychology,
                              size: 16,
                              color: TemaBoho.colorPrimario,
                            ),
                            const SizedBox(width: 6),
                            Text(
                              conexionIA ? 'IA recomienda:' : 'Sugerencias locales:',
                              style: TextStyle(
                                color: TemaBoho.colorPrimario,
                                fontWeight: FontWeight.w600,
                                fontSize: 12,
                              ),
                            ),
                          ],
                        ),
                        const SizedBox(height: 6),
                        Wrap(
                          spacing: 6,
                          children: sugerenciasIA.map((chemical) {
                            return Container(
                              padding: const EdgeInsets.symmetric(
                                horizontal: 8,
                                vertical: 4,
                              ),
                              decoration: BoxDecoration(
                                color: TemaBoho.colorPrimario.withOpacity(0.2),
                                borderRadius: BorderRadius.circular(10),
                              ),
                              child: Text(
                                chemical,
                                style: TextStyle(
                                  color: TemaBoho.colorPrimario,
                                  fontSize: 11,
                                  fontWeight: FontWeight.w500,
                                ),
                              ),
                            );
                          }).toList(),
                        ),
                      ],
                    ),
                  ),
                ],
                
                const SizedBox(height: 16),
                
                // Panel de Natural Chemicals
                PanelNaturalChemicals(
                  onNaturalChemicalCompletado: (datos) async {
                    // Actualizar estado emocional con IA
                    await ref.read(moodmapConIAProvider.notifier)
                        .actualizarPorActividad(
                      tipoChemical: datos['chemical'],
                      nombreActividad: datos['titulo'],
                      intensidad: datos['intensidad'],
                      notas: datos['notas'],
                    );
                    
                    setState(() {
                      _naturalChemicalSeleccionado = datos;
                      _mostrarFeedback = true;
                    });
                  },
                ),
              ],
            ),
          ],

          // Widget de feedback post-acción con IA
          if (_mostrarFeedback && _naturalChemicalSeleccionado != null) ...[
            const SizedBox(height: 20),
            Container(
              padding: const EdgeInsets.all(24),
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.circular(25),
                boxShadow: TemaBoho.obtenerSombraRelieve(),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      const Icon(
                        Icons.celebration,
                        color: TemaBoho.colorPrimario,
                        size: 28,
                      ),
                      const SizedBox(width: 12),
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              '¡Natural Chemical Completado!',
                              style: Theme.of(context).textTheme.titleLarge,
                            ),
                            if (conexionIA)
                              Text(
                                'Análisis actualizado con IA',
                                style: Theme.of(context).textTheme.bodySmall?.copyWith(
                                  color: Colors.green,
                                  fontWeight: FontWeight.w600,
                                ),
                              ),
                          ],
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 16),
                  
                  Text(
                    'Actividad: ${_naturalChemicalSeleccionado!['titulo']}',
                    style: Theme.of(context).textTheme.titleMedium?.copyWith(
                      color: TemaBoho.colorPrimario,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                  const SizedBox(height: 8),
                  
                  // Mostrar mejoras predichas
                  Container(
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: Colors.green.withOpacity(0.1),
                      borderRadius: BorderRadius.circular(10),
                      border: Border.all(
                        color: Colors.green.withOpacity(0.3),
                      ),
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          'Mejoras detectadas:',
                          style: TextStyle(
                            color: Colors.green.shade700,
                            fontWeight: FontWeight.w600,
                            fontSize: 14,
                          ),
                        ),
                        const SizedBox(height: 8),
                        _construirIndicadorMejora('Felicidad', moodmap.felicidad),
                        _construirIndicadorMejora('Estrés', 1.0 - moodmap.estres),
                        _construirIndicadorMejora('Motivación', moodmap.motivacion),
                      ],
                    ),
                  ),
                  
                  const SizedBox(height: 12),
                  
                  Row(
                    children: [
                      Text('Intensidad aplicada: '),
                      Row(
                        children: List.generate(_naturalChemicalSeleccionado!['intensidad'], (index) {
                          return Container(
                            margin: const EdgeInsets.only(right: 4),
                            width: 20,
                            height: 20,
                            decoration: const BoxDecoration(
                              shape: BoxShape.circle,
                              color: TemaBoho.colorFelicidad,
                            ),
                            child: Center(
                              child: Text(
                                '${index + 1}',
                                style: const TextStyle(
                                  color: Colors.white,
                                  fontSize: 12,
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                            ),
                          );
                        }),
                      ),
                    ],
                  ),
                  
                  if (_naturalChemicalSeleccionado!['notas'].toString().isNotEmpty) ...[
                    const SizedBox(height: 12),
                    Text(
                      'Notas: ${_naturalChemicalSeleccionado!['notas']}',
                      style: Theme.of(context).textTheme.bodyMedium,
                    ),
                  ],
                  
                  const SizedBox(height: 20),
                  
                  SizedBox(
                    width: double.infinity,
                    child: ElevatedButton(
                      onPressed: () {
                        setState(() {
                          _mostrarFeedback = false;
                          _naturalChemicalSeleccionado = null;
                        });
                        
                        ScaffoldMessenger.of(context).showSnackBar(
                          SnackBar(
                            content: Text(
                              conexionIA 
                                ? '¡Excelente! IA ha actualizado tu perfil emocional ✨'
                                : '¡Excelente trabajo activando tus químicos naturales! ✨'
                            ),
                            backgroundColor: TemaBoho.colorPrimario,
                            behavior: SnackBarBehavior.floating,
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(10),
                            ),
                          ),
                        );
                      },
                      style: ElevatedButton.styleFrom(
                        backgroundColor: TemaBoho.colorPrimario,
                        padding: const EdgeInsets.symmetric(vertical: 16),
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(15),
                        ),
                      ),
                      child: const Text(
                        'Continuar',
                        style: TextStyle(
                          color: Colors.white,
                          fontWeight: FontWeight.w600,
                          fontSize: 16,
                        ),
                      ),
                    ),
                  ),
                ],
              ),
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

  /// Construye un indicador de mejora emocional
  Widget _construirIndicadorMejora(String label, double valor) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 4),
      child: Row(
        children: [
          SizedBox(
            width: 80,
            child: Text(
              label,
              style: const TextStyle(fontSize: 12),
            ),
          ),
          Expanded(
            child: LinearProgressIndicator(
              value: valor,
              backgroundColor: Colors.grey.withOpacity(0.3),
              valueColor: AlwaysStoppedAnimation<Color>(
                valor > 0.7 ? Colors.green : 
                valor > 0.4 ? Colors.orange : Colors.red,
              ),
            ),
          ),
          const SizedBox(width: 8),
          Text(
            '${(valor * 100).toInt()}%',
            style: const TextStyle(
              fontSize: 12,
              fontWeight: FontWeight.w600,
            ),
          ),
        ],
      ),
    );
  }
}
