import 'package:flutter/material.dart';
import '../theme/tema_boho.dart';

/// Widget para liberar emociones tóxicas mediante gestos táctiles
class LiberacionEmocionesWidget extends StatefulWidget {
  final List<String> emocionesLiberadas;
  final Function(String) onEmocionLiberada;

  const LiberacionEmocionesWidget({
    super.key,
    required this.emocionesLiberadas,
    required this.onEmocionLiberada,
  });

  @override
  State<LiberacionEmocionesWidget> createState() =>
      _LiberacionEmocionesWidgetState();
}

class _LiberacionEmocionesWidgetState
    extends State<LiberacionEmocionesWidget> {
  final TextEditingController _emocionController = TextEditingController();
  final List<String> _emocionesDisponibles = [
    'ansiedad',
    'miedo',
    'frustración',
    'preocupación',
    'tristeza',
    'ira',
    'culpa',
    'vergüenza',
  ];

  @override
  void dispose() {
    _emocionController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        // Campo para escribir emoción personalizada
        TextField(
          controller: _emocionController,
          decoration: InputDecoration(
            hintText: 'Escribe una emoción que quieras liberar...',
            hintStyle: TextStyle(
              color: TemaBoho.colorTexto.withOpacity(0.5),
            ),
            prefixIcon: const Icon(
              Icons.psychology,
              color: TemaBoho.colorEstres,
            ),
            suffixIcon: IconButton(
              icon: const Icon(
                Icons.send,
                color: TemaBoho.colorEstres,
              ),
              onPressed: () {
                if (_emocionController.text.isNotEmpty) {
                  widget.onEmocionLiberada(_emocionController.text);
                  _emocionController.clear();
                }
              },
            ),
          ),
          onSubmitted: (value) {
            if (value.isNotEmpty) {
              widget.onEmocionLiberada(value);
              _emocionController.clear();
            }
          },
        ),

        const SizedBox(height: 20),

        // Emociones sugeridas
        Text(
          'O selecciona una emoción:',
          style: Theme.of(context).textTheme.bodySmall?.copyWith(
                color: TemaBoho.colorTexto.withOpacity(0.7),
              ),
        ),
        const SizedBox(height: 12),

        // Grid de emociones arrastrables
        Wrap(
          spacing: 10,
          runSpacing: 10,
          children: _emocionesDisponibles.map((emocion) {
            final yaLiberada = widget.emocionesLiberadas.contains(emocion);
            return _construirChipEmocion(emocion, yaLiberada);
          }).toList(),
        ),

        const SizedBox(height: 20),

        // Zona de liberación (arrastrar aquí)
        _construirZonaLiberacion(),
      ],
    );
  }

  /// Construye un chip de emoción arrastrable
  Widget _construirChipEmocion(String emocion, bool liberada) {
    return Draggable<String>(
      data: emocion,
      feedback: Material(
        color: Colors.transparent,
        child: _construirContenidoChip(emocion, true),
      ),
      childWhenDragging: Opacity(
        opacity: 0.3,
        child: _construirContenidoChip(emocion, liberada),
      ),
      child: _construirContenidoChip(emocion, liberada),
    );
  }

  /// Construye el contenido visual del chip
  Widget _construirContenidoChip(String emocion, bool liberada) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
      decoration: BoxDecoration(
        gradient: liberada
            ? LinearGradient(
                colors: [
                  TemaBoho.colorMotivacion.withOpacity(0.3),
                  TemaBoho.colorMotivacion.withOpacity(0.1),
                ],
              )
            : LinearGradient(
                colors: [
                  TemaBoho.colorEstres.withOpacity(0.6),
                  TemaBoho.colorEstres.withOpacity(0.4),
                ],
              ),
        borderRadius: BorderRadius.circular(20),
        border: Border.all(
          color: liberada
              ? TemaBoho.colorMotivacion.withOpacity(0.5)
              : TemaBoho.colorEstres.withOpacity(0.5),
          width: 1.5,
        ),
        boxShadow: liberada
            ? []
            : [
                BoxShadow(
                  color: TemaBoho.colorEstres.withOpacity(0.3),
                  blurRadius: 8,
                  offset: const Offset(0, 4),
                ),
              ],
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(
            liberada ? Icons.check_circle : Icons.cloud,
            color: liberada
                ? TemaBoho.colorMotivacion
                : Colors.white,
            size: 18,
          ),
          const SizedBox(width: 6),
          Text(
            emocion,
            style: TextStyle(
              color: liberada
                  ? TemaBoho.colorMotivacion
                  : Colors.white,
              fontWeight: FontWeight.w500,
              decoration: liberada ? TextDecoration.lineThrough : null,
            ),
          ),
        ],
      ),
    );
  }

  /// Construye la zona donde se arrastra para liberar
  Widget _construirZonaLiberacion() {
    return DragTarget<String>(
      onAccept: (emocion) {
        widget.onEmocionLiberada(emocion);
      },
      builder: (context, candidateData, rejectedData) {
        final isDragging = candidateData.isNotEmpty;
        
        return AnimatedContainer(
          duration: const Duration(milliseconds: 300),
          height: 120,
          decoration: BoxDecoration(
            gradient: LinearGradient(
              begin: Alignment.topLeft,
              end: Alignment.bottomRight,
              colors: isDragging
                  ? [
                      TemaBoho.colorMotivacion.withOpacity(0.3),
                      TemaBoho.colorMotivacion.withOpacity(0.1),
                    ]
                  : [
                      TemaBoho.colorAcento.withOpacity(0.1),
                      TemaBoho.colorAcento.withOpacity(0.05),
                    ],
            ),
            borderRadius: BorderRadius.circular(20),
            border: Border.all(
              color: isDragging
                  ? TemaBoho.colorMotivacion
                  : TemaBoho.colorAcento.withOpacity(0.3),
              width: 2,
              style: BorderStyle.solid,
            ),
          ),
          child: Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Icon(
                  isDragging ? Icons.auto_awesome : Icons.cloud_upload,
                  color: isDragging
                      ? TemaBoho.colorMotivacion
                      : TemaBoho.colorAcento,
                  size: 40,
                ),
                const SizedBox(height: 8),
                Text(
                  isDragging
                      ? '¡Suelta aquí para liberar!'
                      : 'Arrastra una emoción aquí',
                  style: TextStyle(
                    color: isDragging
                        ? TemaBoho.colorMotivacion
                        : TemaBoho.colorTexto.withOpacity(0.7),
                    fontWeight: FontWeight.w500,
                  ),
                ),
                if (isDragging) ...[
                  const SizedBox(height: 4),
                  Text(
                    '✨ Dejar ir y fluir ✨',
                    style: TextStyle(
                      color: TemaBoho.colorMotivacion.withOpacity(0.8),
                      fontSize: 12,
                      fontStyle: FontStyle.italic,
                    ),
                  ),
                ],
              ],
            ),
          ),
        );
      },
    );
  }
}
