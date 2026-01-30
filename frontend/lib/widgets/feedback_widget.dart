import 'package:flutter/material.dart';
import '../theme/tema_boho.dart';

/// Widget de feedback post-acción
/// Incluye sliders de evaluación y campo de texto libre
class FeedbackWidget extends StatefulWidget {
  final String microaccion;
  final Function() onFeedbackEnviado;

  const FeedbackWidget({
    super.key,
    required this.microaccion,
    required this.onFeedbackEnviado,
  });

  @override
  State<FeedbackWidget> createState() => _FeedbackWidgetState();
}

class _FeedbackWidgetState extends State<FeedbackWidget>
    with SingleTickerProviderStateMixin {
  double _efectividad = 3.0; // 1-5
  double _comodidad = 3.0; // 1-5
  double _energia = 3.0; // 1-5
  final TextEditingController _comentarioController = TextEditingController();
  
  late AnimationController _animationController;
  late Animation<double> _slideAnimation;

  @override
  void initState() {
    super.initState();
    _animationController = AnimationController(
      duration: const Duration(milliseconds: 600),
      vsync: this,
    );
    _slideAnimation = CurvedAnimation(
      parent: _animationController,
      curve: Curves.easeOutCubic,
    );
    _animationController.forward();
  }

  @override
  void dispose() {
    _animationController.dispose();
    _comentarioController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return SlideTransition(
      position: Tween<Offset>(
        begin: const Offset(0, 0.5),
        end: Offset.zero,
      ).animate(_slideAnimation),
      child: FadeTransition(
        opacity: _slideAnimation,
        child: Container(
          padding: const EdgeInsets.all(24),
          decoration: BoxDecoration(
            color: Colors.white,
            borderRadius: BorderRadius.circular(25),
            boxShadow: TemaBoho.obtenerSombraRelieve(),
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Título
              Row(
                children: [
                  const Icon(
                    Icons.feedback,
                    color: TemaBoho.colorPrimario,
                    size: 28,
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: Text(
                      '¿Cómo te sentiste?',
                      style: Theme.of(context).textTheme.titleLarge,
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 8),
              Text(
                'Microacción: ${_nombreMicroaccion(widget.microaccion)}',
                style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                      color: TemaBoho.colorTexto.withOpacity(0.7),
                    ),
              ),

              const SizedBox(height: 24),

              // Slider de efectividad
              _construirSlider(
                'Efectividad',
                'Qué tan útil fue',
                Icons.stars,
                _efectividad,
                TemaBoho.colorMotivacion,
                (valor) => setState(() => _efectividad = valor),
              ),

              const SizedBox(height: 20),

              // Slider de comodidad
              _construirSlider(
                'Comodidad',
                'Qué tan cómoda fue',
                Icons.favorite,
                _comodidad,
                TemaBoho.colorFelicidad,
                (valor) => setState(() => _comodidad = valor),
              ),

              const SizedBox(height: 20),

              // Slider de energía
              _construirSlider(
                'Energía',
                'Cómo afectó tu energía',
                Icons.bolt,
                _energia,
                TemaBoho.colorTerciario,
                (valor) => setState(() => _energia = valor),
              ),

              const SizedBox(height: 24),

              // Campo de comentario libre
              TextField(
                controller: _comentarioController,
                maxLines: 3,
                decoration: InputDecoration(
                  hintText: 'Comparte tus pensamientos (opcional)...',
                  hintStyle: TextStyle(
                    color: TemaBoho.colorTexto.withOpacity(0.5),
                  ),
                  prefixIcon: const Icon(
                    Icons.edit_note,
                    color: TemaBoho.colorPrimario,
                  ),
                ),
              ),

              const SizedBox(height: 24),

              // Botón de enviar
              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  onPressed: _enviarFeedback,
                  style: ElevatedButton.styleFrom(
                    backgroundColor: TemaBoho.colorPrimario,
                    foregroundColor: Colors.white,
                    padding: const EdgeInsets.symmetric(vertical: 16),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(15),
                    ),
                    elevation: 6,
                  ),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      const Icon(Icons.send),
                      const SizedBox(width: 8),
                      Text(
                        'Enviar feedback',
                        style: Theme.of(context).textTheme.labelLarge,
                      ),
                    ],
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  /// Construye un slider con etiqueta e icono
  Widget _construirSlider(
    String titulo,
    String descripcion,
    IconData icono,
    double valor,
    Color color,
    Function(double) onChanged,
  ) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          children: [
            Icon(icono, color: color, size: 20),
            const SizedBox(width: 8),
            Text(
              titulo,
              style: Theme.of(context).textTheme.titleSmall?.copyWith(
                    color: color,
                    fontWeight: FontWeight.w600,
                  ),
            ),
          ],
        ),
        const SizedBox(height: 4),
        Text(
          descripcion,
          style: Theme.of(context).textTheme.bodySmall?.copyWith(
                color: TemaBoho.colorTexto.withOpacity(0.6),
                fontSize: 12,
              ),
        ),
        const SizedBox(height: 8),
        Row(
          children: [
            Expanded(
              child: SliderTheme(
                data: SliderTheme.of(context).copyWith(
                  activeTrackColor: color,
                  inactiveTrackColor: color.withOpacity(0.3),
                  thumbColor: color,
                  overlayColor: color.withOpacity(0.2),
                  trackHeight: 6,
                  thumbShape: const RoundSliderThumbShape(
                    enabledThumbRadius: 10,
                  ),
                ),
                child: Slider(
                  value: valor,
                  min: 1,
                  max: 5,
                  divisions: 4,
                  onChanged: onChanged,
                ),
              ),
            ),
            const SizedBox(width: 12),
            Container(
              width: 40,
              height: 40,
              decoration: BoxDecoration(
                color: color.withOpacity(0.2),
                shape: BoxShape.circle,
              ),
              child: Center(
                child: Text(
                  valor.toInt().toString(),
                  style: TextStyle(
                    color: color,
                    fontWeight: FontWeight.bold,
                    fontSize: 16,
                  ),
                ),
              ),
            ),
          ],
        ),
      ],
    );
  }

  /// Obtiene el nombre legible de la microacción
  String _nombreMicroaccion(String accion) {
    switch (accion) {
      case 'calmarse':
        return 'Calmar la mente';
      case 'animarse':
        return 'Animar el espíritu';
      case 'activarse':
        return 'Activar la energía';
      default:
        return accion;
    }
  }

  /// Envía el feedback y cierra el widget
  void _enviarFeedback() {
    // Aquí se enviaría el feedback al backend
    // Por ahora solo mostramos los valores
    print('Feedback enviado:');
    print('Microacción: ${widget.microaccion}');
    print('Efectividad: $_efectividad');
    print('Comodidad: $_comodidad');
    print('Energía: $_energia');
    print('Comentario: ${_comentarioController.text}');

    widget.onFeedbackEnviado();
  }
}
