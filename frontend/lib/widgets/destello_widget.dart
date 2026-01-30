import 'package:flutter/material.dart';
import 'dart:math' as math;
import '../models/usuario_model.dart';
import '../theme/tema_boho.dart';

/// Widget de destello de luz personalizable con efectos visuales
class DestelloWidget extends StatefulWidget {
  final Destello destello;
  final Offset posicion;

  const DestelloWidget({
    super.key,
    required this.destello,
    required this.posicion,
  });

  @override
  State<DestelloWidget> createState() => _DestelloWidgetState();
}

class _DestelloWidgetState extends State<DestelloWidget>
    with TickerProviderStateMixin {
  late AnimationController _floatController;
  late AnimationController _glowController;
  late Animation<double> _floatAnimation;
  late Animation<double> _glowAnimation;

  @override
  void initState() {
    super.initState();

    // Animación de flotación
    _floatController = AnimationController(
      duration: const Duration(milliseconds: 3000),
      vsync: this,
    )..repeat(reverse: true);

    _floatAnimation = Tween<double>(begin: -15, end: 15).animate(
      CurvedAnimation(
        parent: _floatController,
        curve: Curves.easeInOut,
      ),
    );

    // Animación de brillo pulsante
    _glowController = AnimationController(
      duration: const Duration(milliseconds: 2000),
      vsync: this,
    )..repeat(reverse: true);

    _glowAnimation = Tween<double>(begin: 0.7, end: 1.0).animate(
      CurvedAnimation(
        parent: _glowController,
        curve: Curves.easeInOut,
      ),
    );
  }

  @override
  void dispose() {
    _floatController.dispose();
    _glowController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final color = _obtenerColor(widget.destello.color);
    final tamano = 60.0 * widget.destello.tamano;

    return Positioned(
      left: widget.posicion.dx,
      top: widget.posicion.dy,
      child: AnimatedBuilder(
        animation: Listenable.merge([_floatAnimation, _glowAnimation]),
        builder: (context, child) {
          return Transform.translate(
            offset: Offset(0, _floatAnimation.value),
            child: Opacity(
              opacity: widget.destello.intensidad * _glowAnimation.value,
              child: Container(
                width: tamano,
                height: tamano,
                decoration: BoxDecoration(
                  boxShadow: TemaBoho.obtenerSombraDestello(color),
                ),
                child: CustomPaint(
                  painter: DestelloPainter(
                    color: color,
                    forma: widget.destello.forma,
                    intensidad: _glowAnimation.value,
                  ),
                ),
              ),
            ),
          );
        },
      ),
    );
  }

  /// Obtiene el color según el nombre
  Color _obtenerColor(String nombreColor) {
    switch (nombreColor.toLowerCase()) {
      case 'amarillo':
        return TemaBoho.colorTerciario;
      case 'verde':
        return TemaBoho.colorMotivacion;
      case 'rosa':
        return TemaBoho.colorPrimario;
      case 'azul':
        return TemaBoho.colorCalma;
      case 'violeta':
        return TemaBoho.colorEstres;
      default:
        return TemaBoho.colorFelicidad;
    }
  }
}

/// Painter personalizado para dibujar diferentes formas de destellos
class DestelloPainter extends CustomPainter {
  final Color color;
  final String forma;
  final double intensidad;

  DestelloPainter({
    required this.color,
    required this.forma,
    required this.intensidad,
  });

  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = color.withOpacity(0.8 * intensidad)
      ..style = PaintingStyle.fill;

    final center = Offset(size.width / 2, size.height / 2);
    final radius = size.width / 2;

    switch (forma.toLowerCase()) {
      case 'estrella':
        _dibujarEstrella(canvas, center, radius, paint);
        break;
      case 'corazon':
        _dibujarCorazon(canvas, center, radius, paint);
        break;
      case 'hoja':
        _dibujarHoja(canvas, center, radius, paint);
        break;
      default:
        // Círculo por defecto
        canvas.drawCircle(center, radius, paint);
        
        // Brillo interno
        final innerPaint = Paint()
          ..color = Colors.white.withOpacity(0.6 * intensidad)
          ..style = PaintingStyle.fill;
        canvas.drawCircle(center, radius * 0.4, innerPaint);
    }
  }

  /// Dibuja una estrella de 5 puntas
  void _dibujarEstrella(Canvas canvas, Offset center, double radius, Paint paint) {
    final path = Path();
    final innerRadius = radius * 0.4;

    for (int i = 0; i < 10; i++) {
      final r = i.isEven ? radius : innerRadius;
      final angle = (i * math.pi / 5) - math.pi / 2;
      final x = center.dx + r * math.cos(angle);
      final y = center.dy + r * math.sin(angle);

      if (i == 0) {
        path.moveTo(x, y);
      } else {
        path.lineTo(x, y);
      }
    }
    path.close();
    canvas.drawPath(path, paint);

    // Brillo central
    final centerPaint = Paint()
      ..color = Colors.white.withOpacity(0.7 * intensidad)
      ..style = PaintingStyle.fill;
    canvas.drawCircle(center, radius * 0.25, centerPaint);
  }

  /// Dibuja un corazón
  void _dibujarCorazon(Canvas canvas, Offset center, double radius, Paint paint) {
    final path = Path();
    final width = radius * 2;
    final height = radius * 1.8;

    path.moveTo(center.dx, center.dy + height * 0.3);
    
    // Lado izquierdo
    path.cubicTo(
      center.dx - width * 0.5, center.dy - height * 0.3,
      center.dx - width * 0.3, center.dy - height * 0.5,
      center.dx, center.dy - height * 0.2,
    );
    
    // Lado derecho
    path.cubicTo(
      center.dx + width * 0.3, center.dy - height * 0.5,
      center.dx + width * 0.5, center.dy - height * 0.3,
      center.dx, center.dy + height * 0.3,
    );

    canvas.drawPath(path, paint);
  }

  /// Dibuja una hoja
  void _dibujarHoja(Canvas canvas, Offset center, double radius, Paint paint) {
    final path = Path();
    
    // Forma de hoja ovalada con punta
    path.moveTo(center.dx, center.dy - radius);
    path.quadraticBezierTo(
      center.dx + radius * 0.7, center.dy - radius * 0.3,
      center.dx, center.dy + radius,
    );
    path.quadraticBezierTo(
      center.dx - radius * 0.7, center.dy - radius * 0.3,
      center.dx, center.dy - radius,
    );

    canvas.drawPath(path, paint);

    // Nervadura central
    final veinPaint = Paint()
      ..color = Colors.white.withOpacity(0.5 * intensidad)
      ..style = PaintingStyle.stroke
      ..strokeWidth = 2;
    
    canvas.drawLine(
      Offset(center.dx, center.dy - radius),
      Offset(center.dx, center.dy + radius),
      veinPaint,
    );
  }

  @override
  bool shouldRepaint(covariant DestelloPainter oldDelegate) {
    return oldDelegate.intensidad != intensidad ||
        oldDelegate.color != color ||
        oldDelegate.forma != forma;
  }
}
