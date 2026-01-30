import 'package:flutter/material.dart';
import 'dart:math' as math;

/// Widget de burbuja para visualizar una emoción
/// Con animaciones, sombras y colores según intensidad
class BurbujaEmocion extends StatelessWidget {
  final String emocion;
  final double valor; // 0.0 - 1.0
  final Color color;
  final IconData icono;

  const BurbujaEmocion({
    super.key,
    required this.emocion,
    required this.valor,
    required this.color,
    required this.icono,
  });

  @override
  Widget build(BuildContext context) {
    // Tamaño de la burbuja según el valor (50-120 px)
    final double tamano = 50 + (valor * 70);
    
    // Opacidad según el valor
    final double opacidad = 0.4 + (valor * 0.6);

    return Container(
      width: tamano,
      height: tamano,
      decoration: BoxDecoration(
        shape: BoxShape.circle,
        gradient: RadialGradient(
          colors: [
            color.withOpacity(opacidad),
            color.withOpacity(opacidad * 0.6),
            color.withOpacity(opacidad * 0.3),
          ],
          stops: const [0.3, 0.7, 1.0],
        ),
        boxShadow: [
          BoxShadow(
            color: color.withOpacity(0.4),
            blurRadius: 20,
            spreadRadius: 5,
            offset: const Offset(0, 8),
          ),
          BoxShadow(
            color: color.withOpacity(0.2),
            blurRadius: 40,
            spreadRadius: 10,
            offset: const Offset(0, 15),
          ),
        ],
      ),
      child: Stack(
        children: [
          // Efecto de brillo
          Positioned(
            top: tamano * 0.15,
            left: tamano * 0.2,
            child: Container(
              width: tamano * 0.3,
              height: tamano * 0.3,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                gradient: RadialGradient(
                  colors: [
                    Colors.white.withOpacity(0.6),
                    Colors.white.withOpacity(0.0),
                  ],
                ),
              ),
            ),
          ),
          
          // Contenido: icono y texto
          Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Icon(
                  icono,
                  color: Colors.white,
                  size: tamano * 0.35,
                ),
                if (tamano > 80) ...[
                  const SizedBox(height: 4),
                  Text(
                    '${(valor * 100).toInt()}%',
                    style: TextStyle(
                      color: Colors.white,
                      fontWeight: FontWeight.bold,
                      fontSize: tamano * 0.15,
                    ),
                  ),
                ],
              ],
            ),
          ),
        ],
      ),
    );
  }
}
