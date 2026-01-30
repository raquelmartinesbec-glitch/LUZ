import 'package:flutter/material.dart';
import '../theme/tema_boho.dart';

/// Panel de Natural Chemicals
/// Químicos naturales para el bienestar emocional
class PanelMicroacciones extends StatefulWidget {
  final Function(Map<String, dynamic>) onNaturalChemicalCompletado;

  const PanelMicroacciones({
    super.key,
    required this.onNaturalChemicalCompletado,
  });

  @override
  State<PanelMicroacciones> createState() => _PanelMicroaccionesState();
}

class _PanelMicroaccionesState extends State<PanelMicroacciones> {
  final Map<String, bool> _expandido = {};
  final Map<String, int> _intensidad = {};
  final Map<String, TextEditingController> _controladores = {};

  // Lista de Natural Chemicals disponibles
  static const List<Map<String, dynamic>> naturalChemicals = [
    {
      'nombre': 'serotonina',
      'titulo': 'Elevar Serotonina',
      'descripcion': 'Químico de la felicidad y bienestar',
      'icono': Icons.sunny,
      'color': TemaBoho.colorFelicidad,
      'actividades': ['Caminar al sol', 'Meditar', 'Ejercicio suave', 'Música relajante']
    },
    {
      'nombre': 'dopamina',
      'titulo': 'Liberar Dopamina',
      'descripcion': 'Neurotransmisor de la motivación',
      'icono': Icons.rocket_launch,
      'color': TemaBoho.colorMotivacion,
      'actividades': ['Completar tareas', 'Logros pequeños', 'Ejercicio', 'Nuevas experiencias']
    },
    {
      'nombre': 'endorfinas',
      'titulo': 'Producir Endorfinas',
      'descripcion': 'Analgésicos naturales del cuerpo',
      'icono': Icons.spa,
      'color': TemaBoho.colorCalma,
      'actividades': ['Ejercicio intenso', 'Risa', 'Chocolate negro', 'Abrazo largo']
    },
    {
      'nombre': 'oxitocina',
      'titulo': 'Generar Oxitocina',
      'descripcion': 'Hormona del amor y conexión',
      'icono': Icons.favorite,
      'color': Colors.pink.shade300,
      'actividades': ['Abrazar', 'Tiempo con seres queridos', 'Actos de bondad', 'Contacto físico']
    },
  ];

  @override
  void initState() {
    super.initState();
    for (var chemical in naturalChemicals) {
      final nombre = chemical['nombre'] as String;
      _expandido[nombre] = false;
      _intensidad[nombre] = 3;
      _controladores[nombre] = TextEditingController();
    }
  }

  @override
  void dispose() {
    for (var controller in _controladores.values) {
      controller.dispose();
    }
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: naturalChemicals.map((chemical) {
        final nombre = chemical['nombre'] as String;
        return _construirTarjetaNaturalChemical(
          context,
          chemical: chemical,
          expandido: _expandido[nombre] ?? false,
          intensidad: _intensidad[nombre] ?? 3,
          controller: _controladores[nombre]!,
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
