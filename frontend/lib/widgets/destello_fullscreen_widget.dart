import 'package:flutter/material.dart';
import 'dart:math' as math;
import '../theme/tema_boho.dart';

/// Widget de destello que ocupa toda la pantalla con efectos de luz espectaculares
class DestelloFullScreenWidget extends StatefulWidget {
  final Color color;
  final String mensaje;

  const DestelloFullScreenWidget({
    super.key,
    required this.color,
    this.mensaje = '¡Destello de luz activado! ✨',
  });

  @override
  State<DestelloFullScreenWidget> createState() => _DestelloFullScreenWidgetState();
}

class _DestelloFullScreenWidgetState extends State<DestelloFullScreenWidget>
    with TickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _scaleAnimation;
  late Animation<double> _opacityAnimation;
  late Animation<double> _rotationAnimation;
  late Animation<double> _pulseAnimation;

  @override
  void initState() {
    super.initState();

    _controller = AnimationController(
      duration: const Duration(milliseconds: 2500),
      vsync: this,
    );

    // Animación de escala (desde centro hacia afuera)
    _scaleAnimation = Tween<double>(
      begin: 0.0,
      end: 2.0,
    ).animate(CurvedAnimation(
      parent: _controller,
      curve: const Interval(0.0, 0.7, curve: Curves.elasticOut),
    ));

    // Animación de opacidad
    _opacityAnimation = Tween<double>(
      begin: 1.0,
      end: 0.0,
    ).animate(CurvedAnimation(
      parent: _controller,
      curve: const Interval(0.6, 1.0, curve: Curves.easeOut),
    ));

    // Animación de rotación
    _rotationAnimation = Tween<double>(
      begin: 0.0,
      end: 1.0,
    ).animate(CurvedAnimation(
      parent: _controller,
      curve: Curves.linear,
    ));

    // Animación de pulso
    _pulseAnimation = Tween<double>(
      begin: 0.8,
      end: 1.2,
    ).animate(CurvedAnimation(
      parent: _controller,
      curve: Curves.easeInOut,
    ));

    // Iniciar animación
    _controller.forward();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Material(
      color: Colors.transparent,
      child: AnimatedBuilder(
        animation: _controller,
        builder: (context, child) {
          return Opacity(
            opacity: _opacityAnimation.value,
            child: Container(
              width: double.infinity,
              height: double.infinity,
              child: Stack(
                children: [
                  // Ondas de luz expandiéndose
                  ...List.generate(5, (index) {
                    return Positioned.fill(
                      child: Transform.scale(
                        scale: _scaleAnimation.value * (1.0 + index * 0.3),
                        child: Opacity(
                          opacity: (1.0 - index * 0.2) * (1.0 - _controller.value),
                          child: Container(
                            decoration: BoxDecoration(
                              shape: BoxShape.circle,
                              border: Border.all(
                                color: widget.color.withOpacity(0.3 - index * 0.05),
                                width: 3.0,
                              ),
                            ),
                          ),
                        ),
                      ),
                    );
                  }),

                  // Destello central giratorio
                  Center(
                    child: Transform.rotate(
                      angle: _rotationAnimation.value * 2 * math.pi,
                      child: Transform.scale(
                        scale: _scaleAnimation.value * _pulseAnimation.value,
                        child: Container(
                          width: 200,
                          height: 200,
                          child: CustomPaint(
                            painter: EstrellaBrillantePainter(
                              color: widget.color,
                              intensidad: 1.0 - _controller.value,
                            ),
                          ),
                        ),
                      ),
                    ),
                  ),

                  // Partículas de luz dispersas
                  ...List.generate(12, (index) {
                    final angle = (index * 30.0) * (math.pi / 180);
                    final distance = 150.0 * _scaleAnimation.value;
                    
                    return Positioned(
                      left: MediaQuery.of(context).size.width / 2 + 
                            math.cos(angle) * distance - 10,
                      top: MediaQuery.of(context).size.height / 2 + 
                           math.sin(angle) * distance - 10,
                      child: Opacity(
                        opacity: (1.0 - _controller.value) * 0.8,
                        child: Container(
                          width: 20,
                          height: 20,
                          decoration: BoxDecoration(
                            shape: BoxShape.circle,
                            color: widget.color.withOpacity(0.7),
                            boxShadow: [
                              BoxShadow(
                                color: widget.color.withOpacity(0.5),
                                blurRadius: 10,
                                spreadRadius: 2,
                              ),
                            ],
                          ),
                        ),
                      ),
                    );
                  }),

                  // Mensaje central
                  if (_controller.value < 0.5)
                    Center(
                      child: Transform.scale(
                        scale: _scaleAnimation.value * 0.5,
                        child: Container(
                          padding: const EdgeInsets.symmetric(
                            horizontal: 24,
                            vertical: 12,
                          ),
                          decoration: BoxDecoration(
                            gradient: LinearGradient(
                              colors: [
                                widget.color.withOpacity(0.9),
                                widget.color.withOpacity(0.7),
                              ],
                            ),
                            borderRadius: BorderRadius.circular(25),
                            boxShadow: [
                              BoxShadow(
                                color: widget.color.withOpacity(0.4),
                                blurRadius: 15,
                                spreadRadius: 3,
                              ),
                            ],
                          ),
                          child: Row(
                            mainAxisSize: MainAxisSize.min,
                            children: [
                              const Icon(
                                Icons.auto_awesome,
                                color: Colors.white,
                                size: 24,
                              ),
                              const SizedBox(width: 8),
                              Text(
                                widget.mensaje,
                                style: const TextStyle(
                                  color: Colors.white,
                                  fontSize: 18,
                                  fontWeight: FontWeight.w600,
                                ),
                              ),
                            ],
                          ),
                        ),
                      ),
                    ),
                ],
              ),
            ),
          );
        },
      ),
    );
  }
}

/// Painter para dibujar una estrella brillante
class EstrellaBrillantePainter extends CustomPainter {
  final Color color;
  final double intensidad;

  EstrellaBrillantePainter({
    required this.color,
    required this.intensidad,
  });

  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = color.withOpacity(intensidad)
      ..style = PaintingStyle.fill;

    final center = Offset(size.width / 2, size.height / 2);
    final radius = size.width / 2;

    // Dibujar estrella de 8 puntas
    final path = Path();
    const numPoints = 8;
    const innerRadius = 0.4;

    for (int i = 0; i < numPoints * 2; i++) {
      final angle = (i * math.pi) / numPoints;
      final r = (i % 2 == 0) ? radius : radius * innerRadius;
      final x = center.dx + r * math.cos(angle - math.pi / 2);
      final y = center.dy + r * math.sin(angle - math.pi / 2);

      if (i == 0) {
        path.moveTo(x, y);
      } else {
        path.lineTo(x, y);
      }
    }
    path.close();

    // Aplicar gradiente radial
    paint.shader = RadialGradient(
      colors: [
        Colors.white.withOpacity(intensidad),
        color.withOpacity(intensidad * 0.8),
        color.withOpacity(intensidad * 0.3),
      ],
      stops: const [0.0, 0.5, 1.0],
    ).createShader(Rect.fromCircle(center: center, radius: radius));

    canvas.drawPath(path, paint);

    // Dibujar resplandor adicional
    paint.shader = null;
    paint.color = color.withOpacity(intensidad * 0.3);
    paint.maskFilter = const MaskFilter.blur(BlurStyle.normal, 10);
    canvas.drawPath(path, paint);
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => true;
}