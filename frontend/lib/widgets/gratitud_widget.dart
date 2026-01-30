import 'package:flutter/material.dart';
import '../theme/tema_boho.dart';

/// Widget para cultivar gratitud y creatividad
class GratitudWidget extends StatefulWidget {
  final List<String> microaccionesGratitud;
  final Function(String) onGratitudAgregada;

  const GratitudWidget({
    super.key,
    required this.microaccionesGratitud,
    required this.onGratitudAgregada,
  });

  @override
  State<GratitudWidget> createState() => _GratitudWidgetState();
}

class _GratitudWidgetState extends State<GratitudWidget> {
  final TextEditingController _gratitudController = TextEditingController();
  
  final List<Map<String, dynamic>> _sugerencias = [
    {
      'texto': 'Escribir 3 cosas por las que estoy agradecido/a',
      'icono': Icons.edit,
    },
    {
      'texto': 'Dibujar una idea creativa',
      'icono': Icons.draw,
    },
    {
      'texto': 'Meditación guiada',
      'icono': Icons.self_improvement,
    },
    {
      'texto': 'Escribir afirmaciones positivas',
      'icono': Icons.favorite,
    },
    {
      'texto': 'Crear una lista de logros',
      'icono': Icons.emoji_events,
    },
    {
      'texto': 'Conectar con la naturaleza',
      'icono': Icons.nature_people,
    },
  ];

  @override
  void dispose() {
    _gratitudController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        // Campo de texto para gratitud personalizada
        TextField(
          controller: _gratitudController,
          decoration: InputDecoration(
            hintText: 'Escribe tu momento de gratitud...',
            hintStyle: TextStyle(
              color: TemaBoho.colorTexto.withOpacity(0.5),
            ),
            prefixIcon: const Icon(
              Icons.auto_awesome,
              color: TemaBoho.colorTerciario,
            ),
            suffixIcon: IconButton(
              icon: const Icon(
                Icons.add_circle,
                color: TemaBoho.colorTerciario,
              ),
              onPressed: () {
                if (_gratitudController.text.isNotEmpty) {
                  widget.onGratitudAgregada(_gratitudController.text);
                  _gratitudController.clear();
                }
              },
            ),
          ),
          onSubmitted: (value) {
            if (value.isNotEmpty) {
              widget.onGratitudAgregada(value);
              _gratitudController.clear();
            }
          },
        ),

        const SizedBox(height: 20),

        // Sugerencias de microacciones
        Text(
          'Sugerencias:',
          style: Theme.of(context).textTheme.bodySmall?.copyWith(
                color: TemaBoho.colorTexto.withOpacity(0.7),
              ),
        ),
        const SizedBox(height: 12),

        // Grid de sugerencias
        GridView.builder(
          shrinkWrap: true,
          physics: const NeverScrollableScrollPhysics(),
          gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
            crossAxisCount: 2,
            crossAxisSpacing: 12,
            mainAxisSpacing: 12,
            childAspectRatio: 1.5,
          ),
          itemCount: _sugerencias.length,
          itemBuilder: (context, index) {
            final sugerencia = _sugerencias[index];
            final yaAgregada = widget.microaccionesGratitud
                .contains(sugerencia['texto']);
            
            return _construirTarjetaSugerencia(
              sugerencia['texto'],
              sugerencia['icono'],
              yaAgregada,
            );
          },
        ),
      ],
    );
  }

  /// Construye una tarjeta de sugerencia de gratitud
  Widget _construirTarjetaSugerencia(
    String texto,
    IconData icono,
    bool agregada,
  ) {
    return GestureDetector(
      onTap: () {
        if (!agregada) {
          widget.onGratitudAgregada(texto);
        }
      },
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 300),
        padding: const EdgeInsets.all(12),
        decoration: BoxDecoration(
          gradient: agregada
              ? LinearGradient(
                  colors: [
                    TemaBoho.colorMotivacion.withOpacity(0.3),
                    TemaBoho.colorMotivacion.withOpacity(0.1),
                  ],
                )
              : LinearGradient(
                  colors: [
                    TemaBoho.colorTerciario.withOpacity(0.2),
                    TemaBoho.colorTerciario.withOpacity(0.05),
                  ],
                ),
          borderRadius: BorderRadius.circular(15),
          border: Border.all(
            color: agregada
                ? TemaBoho.colorMotivacion.withOpacity(0.5)
                : TemaBoho.colorTerciario.withOpacity(0.5),
            width: 1.5,
          ),
          boxShadow: agregada
              ? [
                  BoxShadow(
                    color: TemaBoho.colorMotivacion.withOpacity(0.3),
                    blurRadius: 12,
                    offset: const Offset(0, 4),
                  ),
                ]
              : [
                  BoxShadow(
                    color: TemaBoho.colorTerciario.withOpacity(0.2),
                    blurRadius: 8,
                    offset: const Offset(0, 2),
                  ),
                ],
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(
              agregada ? Icons.check_circle : icono,
              color: agregada
                  ? TemaBoho.colorMotivacion
                  : TemaBoho.colorTerciario,
              size: 32,
            ),
            const SizedBox(height: 8),
            Text(
              texto,
              textAlign: TextAlign.center,
              style: Theme.of(context).textTheme.bodySmall?.copyWith(
                    color: agregada
                        ? TemaBoho.colorMotivacion
                        : TemaBoho.colorTexto,
                    fontSize: 11,
                    height: 1.3,
                  ),
              maxLines: 3,
              overflow: TextOverflow.ellipsis,
            ),
          ],
        ),
      ),
    );
  }
}
