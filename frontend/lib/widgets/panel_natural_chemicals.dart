import 'package:flutter/material.dart';
import '../theme/tema_boho.dart';

/// Panel de Natural Chemicals
/// Químicos naturales para el bienestar emocional
class PanelNaturalChemicals extends StatefulWidget {
  final Function(Map<String, dynamic>) onNaturalChemicalCompletado;

  const PanelNaturalChemicals({
    super.key,
    required this.onNaturalChemicalCompletado,
  });

  @override
  State<PanelNaturalChemicals> createState() => _PanelNaturalChemicalsState();
}

class _PanelNaturalChemicalsState extends State<PanelNaturalChemicals> {
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
      'color': Colors.pink,
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

  /// Construye una tarjeta de Natural Chemical con desplegable
  Widget _construirTarjetaNaturalChemical(
    BuildContext context, {
    required Map<String, dynamic> chemical,
    required bool expandido,
    required int intensidad,
    required TextEditingController controller,
  }) {
    final nombre = chemical['nombre'] as String;
    final titulo = chemical['titulo'] as String;
    final descripcion = chemical['descripcion'] as String;
    final icono = chemical['icono'] as IconData;
    final color = chemical['color'] as Color;
    final actividades = chemical['actividades'] as List<String>;

    return AnimatedContainer(
      duration: const Duration(milliseconds: 300),
      margin: const EdgeInsets.only(bottom: 16),
      child: Material(
        color: Colors.transparent,
        child: Container(
          decoration: BoxDecoration(
            color: Colors.white,
            borderRadius: BorderRadius.circular(20),
            border: Border.all(
              color: expandido ? color : color.withOpacity(0.3),
              width: 2,
            ),
            boxShadow: [
              BoxShadow(
                color: color.withOpacity(expandido ? 0.3 : 0.1),
                blurRadius: 15,
                offset: const Offset(0, 5),
              ),
            ],
          ),
          child: Column(
            children: [
              // Header clickeable
              InkWell(
                onTap: () {
                  setState(() {
                    _expandido[nombre] = !_expandido[nombre]!;
                  });
                },
                borderRadius: BorderRadius.circular(20),
                child: Padding(
                  padding: const EdgeInsets.all(20),
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
                      
                      // Información del chemical
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
                      AnimatedRotation(
                        turns: expandido ? 0.25 : 0,
                        duration: const Duration(milliseconds: 200),
                        child: Icon(
                          Icons.keyboard_arrow_down,
                          color: color.withOpacity(0.7),
                          size: 24,
                        ),
                      ),
                    ],
                  ),
                ),
              ),
              
              // Contenido expandible
              if (expandido) _construirContenidoExpandido(
                context,
                nombre: nombre,
                actividades: actividades,
                intensidad: intensidad,
                controller: controller,
                color: color,
              ),
            ],
          ),
        ),
      ),
    );
  }

  /// Construye el contenido expandido con actividades, intensidad y texto
  Widget _construirContenidoExpandido(
    BuildContext context, {
    required String nombre,
    required List<String> actividades,
    required int intensidad,
    required TextEditingController controller,
    required Color color,
  }) {
    return Container(
      padding: const EdgeInsets.fromLTRB(20, 0, 20, 20),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Divider(height: 1),
          const SizedBox(height: 16),
          
          // Selector de actividad
          Text(
            'Actividades sugeridas:',
            style: Theme.of(context).textTheme.titleSmall?.copyWith(
              color: color,
              fontWeight: FontWeight.w600,
            ),
          ),
          const SizedBox(height: 8),
          
          Wrap(
            spacing: 8,
            runSpacing: 8,
            children: actividades.map((actividad) {
              return Container(
                padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                decoration: BoxDecoration(
                  color: color.withOpacity(0.1),
                  borderRadius: BorderRadius.circular(20),
                  border: Border.all(color: color.withOpacity(0.3)),
                ),
                child: Text(
                  actividad,
                  style: Theme.of(context).textTheme.bodySmall?.copyWith(
                    color: color,
                    fontWeight: FontWeight.w500,
                  ),
                ),
              );
            }).toList(),
          ),
          
          const SizedBox(height: 20),
          
          // Selector de intensidad con burbujas
          Text(
            'Intensidad (1-5):',
            style: Theme.of(context).textTheme.titleSmall?.copyWith(
              color: color,
              fontWeight: FontWeight.w600,
            ),
          ),
          const SizedBox(height: 12),
          
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            children: List.generate(5, (index) {
              final nivel = index + 1;
              final isSelected = nivel == intensidad;
              
              return GestureDetector(
                onTap: () {
                  setState(() {
                    _intensidad[nombre] = nivel;
                  });
                },
                child: AnimatedContainer(
                  duration: const Duration(milliseconds: 200),
                  width: isSelected ? 50 : 40,
                  height: isSelected ? 50 : 40,
                  decoration: BoxDecoration(
                    shape: BoxShape.circle,
                    color: isSelected ? color : color.withOpacity(0.2),
                    boxShadow: isSelected ? [
                      BoxShadow(
                        color: color.withOpacity(0.4),
                        blurRadius: 8,
                        offset: const Offset(0, 4),
                      ),
                    ] : [],
                  ),
                  child: Center(
                    child: Text(
                      nivel.toString(),
                      style: TextStyle(
                        color: isSelected ? Colors.white : color,
                        fontWeight: FontWeight.bold,
                        fontSize: isSelected ? 18 : 14,
                      ),
                    ),
                  ),
                ),
              );
            }),
          ),
          
          const SizedBox(height: 20),
          
          // Campo de texto opcional
          Text(
            'Notas (opcional):',
            style: Theme.of(context).textTheme.titleSmall?.copyWith(
              color: color,
              fontWeight: FontWeight.w600,
            ),
          ),
          const SizedBox(height: 8),
          
          TextField(
            controller: controller,
            maxLines: 3,
            decoration: InputDecoration(
              hintText: 'Escribe tus pensamientos o experiencia...',
              filled: true,
              fillColor: color.withOpacity(0.05),
              border: OutlineInputBorder(
                borderRadius: BorderRadius.circular(15),
                borderSide: BorderSide(color: color.withOpacity(0.3)),
              ),
              focusedBorder: OutlineInputBorder(
                borderRadius: BorderRadius.circular(15),
                borderSide: BorderSide(color: color, width: 2),
              ),
              enabledBorder: OutlineInputBorder(
                borderRadius: BorderRadius.circular(15),
                borderSide: BorderSide(color: color.withOpacity(0.3)),
              ),
            ),
          ),
          
          const SizedBox(height: 16),
          
          // Botón de completar
          SizedBox(
            width: double.infinity,
            child: ElevatedButton(
              onPressed: () {
                final datos = {
                  'chemical': nombre,
                  'intensidad': intensidad,
                  'notas': controller.text,
                  'titulo': actividades.isNotEmpty ? 'Activé ${nombre}' : 'Chemical completado',
                };
                widget.onNaturalChemicalCompletado(datos);
              },
              style: ElevatedButton.styleFrom(
                backgroundColor: color,
                padding: const EdgeInsets.symmetric(vertical: 16),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(15),
                ),
                elevation: 4,
              ),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const Icon(Icons.check_circle, color: Colors.white),
                  const SizedBox(width: 8),
                  Text(
                    'Completar Chemical',
                    style: const TextStyle(
                      color: Colors.white,
                      fontWeight: FontWeight.w600,
                      fontSize: 16,
                    ),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}