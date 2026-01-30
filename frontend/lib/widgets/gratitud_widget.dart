import 'package:flutter/material.dart';
import '../theme/tema_boho.dart';

/// Widget para cultivar gratitud y creatividad
class GratitudWidget extends StatefulWidget {
  final List<String> microaccionesGratitud;
  final Function(String) onGratitudAgregada;
  final Function(String)? onGratitudSeleccionada;

  const GratitudWidget({
    super.key,
    required this.microaccionesGratitud,
    required this.onGratitudAgregada,
    this.onGratitudSeleccionada,
  });

  @override
  State<GratitudWidget> createState() => _GratitudWidgetState();
}

class _GratitudWidgetState extends State<GratitudWidget>
    with TickerProviderStateMixin {
  final TextEditingController _gratitudController = TextEditingController();
  late AnimationController _animationController;
  late Animation<double> _scaleAnimation;

  @override
  void initState() {
    super.initState();
    _animationController = AnimationController(
      duration: const Duration(milliseconds: 600),
      vsync: this,
    );
    _scaleAnimation = Tween<double>(begin: 0.0, end: 1.0).animate(
      CurvedAnimation(
        parent: _animationController,
        curve: Curves.elasticOut,
      ),
    );
  }

  @override
  void dispose() {
    _gratitudController.dispose();
    _animationController.dispose();
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
                  _animationController.forward().then((_) {
                    _animationController.reset();
                  });
                }
              },
            ),
          ),
          onSubmitted: (value) {
            if (value.isNotEmpty) {
              widget.onGratitudAgregada(value);
              _gratitudController.clear();
              _animationController.forward().then((_) {
                _animationController.reset();
              });
            }
          },
        ),

        const SizedBox(height: 30),

        // Mostrar gratitudes como burbujas
        if (widget.microaccionesGratitud.isNotEmpty)
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                'Tus momentos de gratitud:',
                style: Theme.of(context).textTheme.titleMedium?.copyWith(
                      color: TemaBoho.colorMotivacion,
                      fontWeight: FontWeight.w600,
                    ),
              ),
              const SizedBox(height: 16),
              _construirBurbujasGratitud(),
            ],
          )
        else
          Container(
            padding: const EdgeInsets.all(20),
            decoration: BoxDecoration(
              color: TemaBoho.colorTerciario.withOpacity(0.1),
              borderRadius: BorderRadius.circular(15),
              border: Border.all(
                color: TemaBoho.colorTerciario.withOpacity(0.3),
                width: 1,
              ),
            ),
            child: Row(
              children: [
                const Icon(
                  Icons.lightbulb_outline,
                  color: TemaBoho.colorTerciario,
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: Text(
                    'Escribe algo por lo que te sientes agradecido/a hoy',
                    style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                          color: TemaBoho.colorTexto.withOpacity(0.7),
                        ),
                  ),
                ),
              ],
            ),
          ),
      ],
    );
  }

  /// Construye las burbujas de gratitud
  Widget _construirBurbujasGratitud() {
    return AnimatedBuilder(
      animation: _scaleAnimation,
      builder: (context, child) {
        return Wrap(
          spacing: 12,
          runSpacing: 12,
          children: widget.microaccionesGratitud.asMap().entries.map((entry) {
            final index = entry.key;
            final gratitud = entry.value;
            
            return Transform.scale(
              scale: index == widget.microaccionesGratitud.length - 1 
                  ? _scaleAnimation.value == 0 ? 1.0 : _scaleAnimation.value
                  : 1.0,
              child: _construirBurbujaGratitud(gratitud, index),
            );
          }).toList(),
        );
      },
    );
  }

  /// Construye una burbuja individual de gratitud
  Widget _construirBurbujaGratitud(String gratitud, int index) {
    // Colores alternados para las burbujas
    final colores = [
      TemaBoho.colorMotivacion,
      TemaBoho.colorTerciario,
      TemaBoho.colorSecundario,
    ];
    final color = colores[index % colores.length];
    
    // Texto corto para mostrar en la burbuja
    final textoCorto = gratitud.length > 30 
        ? '${gratitud.substring(0, 30)}...'
        : gratitud;
    
    return GestureDetector(
      onTap: () {
        _mostrarGratitudCompleta(gratitud);
      },
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
        decoration: BoxDecoration(
          gradient: LinearGradient(
            colors: [
              color.withOpacity(0.8),
              color.withOpacity(0.6),
            ],
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
          ),
          borderRadius: BorderRadius.circular(25),
          boxShadow: [
            BoxShadow(
              color: color.withOpacity(0.3),
              blurRadius: 8,
              offset: const Offset(0, 4),
            ),
          ],
        ),
        child: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(
              Icons.favorite,
              color: Colors.white,
              size: 16,
            ),
            const SizedBox(width: 8),
            Flexible(
              child: Text(
                textoCorto,
                style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                      color: Colors.white,
                      fontWeight: FontWeight.w500,
                    ),
                overflow: TextOverflow.ellipsis,
              ),
            ),
          ],
        ),
      ),
    );
  }

  /// Muestra el texto completo de gratitud en un diálogo
  void _mostrarGratitudCompleta(String gratitud) {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(20),
          ),
          title: Row(
            children: [
              const Icon(
                Icons.auto_awesome,
                color: TemaBoho.colorMotivacion,
              ),
              const SizedBox(width: 8),
              const Text('Momento de Gratitud'),
            ],
          ),
          content: Container(
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              gradient: LinearGradient(
                colors: [
                  TemaBoho.colorMotivacion.withOpacity(0.1),
                  TemaBoho.colorTerciario.withOpacity(0.1),
                ],
              ),
              borderRadius: BorderRadius.circular(15),
            ),
            child: Text(
              gratitud,
              style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                    color: TemaBoho.colorTexto,
                    height: 1.5,
                  ),
            ),
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.of(context).pop(),
              child: Text(
                'Cerrar',
                style: TextStyle(color: TemaBoho.colorMotivacion),
              ),
            ),
          ],
        );
      },
    );
  }
}
