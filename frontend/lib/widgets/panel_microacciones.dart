import 'package:flutter/material.dart';
import '../theme/tema_boho.dart';

/// Panel de microacciones adaptativas
/// Sugiere acciones según el estado emocional del usuario
class PanelMicroacciones extends StatelessWidget {
  final Function(String) onMicroaccionSeleccionada;

  const PanelMicroacciones({
    super.key,
    required this.onMicroaccionSeleccionada,
  });

  // Lista de microacciones disponibles
  static const List<Map<String, dynamic>> microacciones = [
    {
      'nombre': 'calmarse',
      'titulo': 'Calmar la mente',
      'descripcion': 'Respiración consciente y meditación',
      'icono': Icons.spa,
      'color': TemaBoho.colorCalma,
    },
    {
      'nombre': 'animarse',
      'titulo': 'Animar el espíritu',
      'descripcion': 'Música y movimiento suave',
      'icono': Icons.music_note,
      'color': TemaBoho.colorFelicidad,
    },
    {
      'nombre': 'activarse',
      'titulo': 'Activar la energía',
      'descripcion': 'Ejercicio y conexión',
      'icono': Icons.directions_run,
      'color': TemaBoho.colorMotivacion,
    },
  ];

  @override
  Widget build(BuildContext context) {
    return Column(
      children: microacciones.map((micro) {
        return _construirTarjetaMicroaccion(
          context,
          nombre: micro['nombre'],
          titulo: micro['titulo'],
          descripcion: micro['descripcion'],
          icono: micro['icono'],
          color: micro['color'],
        );
      }).toList(),
    );
  }

  /// Construye una tarjeta de microacción con animación
  Widget _construirTarjetaMicroaccion(
    BuildContext context, {
    required String nombre,
    required String titulo,
    required String descripcion,
    required IconData icono,
    required Color color,
  }) {
    return Container(
      margin: const EdgeInsets.only(bottom: 16),
      child: Material(
        color: Colors.transparent,
        child: InkWell(
          onTap: () => onMicroaccionSeleccionada(nombre),
          borderRadius: BorderRadius.circular(20),
          child: Container(
            padding: const EdgeInsets.all(20),
            decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.circular(20),
              border: Border.all(
                color: color.withOpacity(0.3),
                width: 2,
              ),
              boxShadow: [
                BoxShadow(
                  color: color.withOpacity(0.2),
                  blurRadius: 15,
                  offset: const Offset(0, 5),
                ),
              ],
            ),
            child: Row(
              children: [
                // Icono con degradado
                Container(
                  width: 60,
                  height: 60,
                  decoration: BoxDecoration(
                    shape: BoxShape.circle,
                    gradient: LinearGradient(
                      colors: [
                        color,
                        color.withOpacity(0.7),
                      ],
                    ),
                    boxShadow: [
                      BoxShadow(
                        color: color.withOpacity(0.4),
                        blurRadius: 10,
                        offset: const Offset(0, 4),
                      ),
                    ],
                  ),
                  child: Icon(
                    icono,
                    color: Colors.white,
                    size: 30,
                  ),
                ),
                
                const SizedBox(width: 16),
                
                // Información de la microacción
                Expanded(
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
                      const SizedBox(height: 4),
                      Text(
                        descripcion,
                        style: Theme.of(context).textTheme.bodySmall?.copyWith(
                              color: TemaBoho.colorTexto.withOpacity(0.7),
                            ),
                      ),
                    ],
                  ),
                ),
                
                // Flecha indicadora
                Icon(
                  Icons.arrow_forward_ios,
                  color: color.withOpacity(0.5),
                  size: 20,
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
