import 'package:flutter/material.dart';
import '../services/seguimiento_microacciones_service.dart';
import '../models/usuario_model.dart';
import '../theme/tema_boho.dart';
import '../widgets/burbuja_emocion.dart';

/// Widget para mostrar recordatorios de seguimiento post-microacción
class RecordatorioSeguimientoWidget extends StatefulWidget {
  final String usuarioId;
  final Function(MoodMapData)? onMoodMapCapturado;

  const RecordatorioSeguimientoWidget({
    Key? key,
    required this.usuarioId,
    this.onMoodMapCapturado,
  }) : super(key: key);

  @override
  State<RecordatorioSeguimientoWidget> createState() => _RecordatorioSeguimientoWidgetState();
}

class _RecordatorioSeguimientoWidgetState extends State<RecordatorioSeguimientoWidget>
    with TickerProviderStateMixin {
  late AnimationController _pulseController;
  late Animation<double> _pulseAnimation;
  
  final SeguimientoMicroaccionesService _seguimientoService = SeguimientoMicroaccionesService();
  List<MicroaccionPendiente> _recordatoriosPendientes = [];
  bool _mostrandoCaptura = false;
  MicroaccionPendiente? _microaccionActual;

  @override
  void initState() {
    super.initState();
    
    _pulseController = AnimationController(
      duration: Duration(seconds: 2),
      vsync: this,
    );
    _pulseAnimation = Tween<double>(
      begin: 1.0,
      end: 1.1,
    ).animate(CurvedAnimation(
      parent: _pulseController,
      curve: Curves.easeInOut,
    ));

    _verificarRecordatorios();
    
    // Verificar cada 30 segundos
    Future.doWhile(() async {
      await Future.delayed(Duration(seconds: 30));
      if (mounted) {
        _verificarRecordatorios();
        return true;
      }
      return false;
    });
  }

  @override
  void dispose() {
    _pulseController.dispose();
    super.dispose();
  }

  void _verificarRecordatorios() {
    final pendientes = _seguimientoService.obtenerRecordatoriosPendientes()
        .where((m) => m.usuarioId == widget.usuarioId)
        .toList();

    if (pendientes.isNotEmpty && pendientes != _recordatoriosPendientes) {
      setState(() {
        _recordatoriosPendientes = pendientes;
      });
      _pulseController.repeat(reverse: true);
    } else if (pendientes.isEmpty && _recordatoriosPendientes.isNotEmpty) {
      setState(() {
        _recordatoriosPendientes = [];
      });
      _pulseController.stop();
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_recordatoriosPendientes.isEmpty) {
      return SizedBox.shrink();
    }

    if (_mostrandoCaptura && _microaccionActual != null) {
      return _buildCapturaMoodmap();
    }

    return _buildRecordatorio();
  }

  Widget _buildRecordatorio() {
    final recordatorio = _recordatoriosPendientes.first;
    
    return Container(
      margin: EdgeInsets.all(16),
      padding: EdgeInsets.all(20),
      decoration: BoxDecoration(
        gradient: LinearGradient(
          colors: [
            BohoColors.terracota.withOpacity(0.1),
            BohoColors.dorado.withOpacity(0.1),
          ],
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
        ),
        borderRadius: BorderRadius.circular(20),
        boxShadow: [
          BoxShadow(
            color: BohoColors.terracota.withOpacity(0.2),
            blurRadius: 15,
            offset: Offset(0, 8),
          ),
        ],
        border: Border.all(
          color: BohoColors.dorado.withOpacity(0.3),
          width: 1,
        ),
      ),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          // Icono animado
          AnimatedBuilder(
            animation: _pulseAnimation,
            builder: (context, child) {
              return Transform.scale(
                scale: _pulseAnimation.value,
                child: Container(
                  padding: EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    color: BohoColors.terracota.withOpacity(0.2),
                    shape: BoxShape.circle,
                  ),
                  child: Icon(
                    Icons.schedule,
                    color: BohoColors.terracota,
                    size: 32,
                  ),
                ),
              );
            },
          ),
          
          SizedBox(height: 16),
          
          // Título
          Text(
            '🌟 ¡Hora de seguimiento!',
            style: TextStyle(
              fontSize: 20,
              fontWeight: FontWeight.bold,
              color: BohoColors.marronOscuro,
            ),
          ),
          
          SizedBox(height: 8),
          
          // Descripción
          Text(
            'Hace ${_formatearTiempo(recordatorio.tiempoTranscurrido)} realizaste:\n\"${_formatearMicroaccion(recordatorio.tipoMicroaccion)}\"',
            textAlign: TextAlign.center,
            style: TextStyle(
              fontSize: 16,
              color: BohoColors.marronOscuro.withOpacity(0.8),
              height: 1.4,
            ),
          ),
          
          SizedBox(height: 20),
          
          // Botones
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            children: [
              // Postponer
              OutlinedButton.icon(
                onPressed: () => _postponerRecordatorio(recordatorio),
                icon: Icon(Icons.schedule_outlined),
                label: Text('5 min más'),
                style: OutlinedButton.styleFrom(
                  foregroundColor: BohoColors.marronOscuro,
                  side: BorderSide(color: BohoColors.marronOscuro.withOpacity(0.5)),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(25),
                  ),
                ),
              ),
              
              // Capturar estado
              ElevatedButton.icon(
                onPressed: () => _iniciarCaptura(recordatorio),
                icon: Icon(Icons.favorite),
                label: Text('¿Cómo estoy?'),
                style: ElevatedButton.styleFrom(
                  backgroundColor: BohoColors.terracota,
                  foregroundColor: Colors.white,
                  elevation: 8,
                  shadowColor: BohoColors.terracota.withOpacity(0.5),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(25),
                  ),
                ),
              ),
            ],
          ),
          
          SizedBox(height: 12),
          
          // Omitir
          TextButton(
            onPressed: () => _omitirRecordatorio(recordatorio),
            child: Text(
              'Omitir esta vez',
              style: TextStyle(
                color: BohoColors.marronOscuro.withOpacity(0.6),
                fontSize: 14,
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildCapturaMoodmap() {
    return Container(
      margin: EdgeInsets.all(16),
      padding: EdgeInsets.all(24),
      decoration: BoxDecoration(
        gradient: LinearGradient(
          colors: [
            BohoColors.verdeOliva.withOpacity(0.1),
            BohoColors.beige.withOpacity(0.1),
          ],
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
        ),
        borderRadius: BorderRadius.circular(20),
        boxShadow: [
          BoxShadow(
            color: BohoColors.verdeOliva.withOpacity(0.2),
            blurRadius: 15,
            offset: Offset(0, 8),
          ),
        ],
      ),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          // Título
          Row(
            children: [
              Icon(
                Icons.psychology,
                color: BohoColors.verdeOliva,
                size: 28,
              ),
              SizedBox(width: 12),
              Expanded(
                child: Text(
                  '¿Cómo te sientes ahora?',
                  style: TextStyle(
                    fontSize: 20,
                    fontWeight: FontWeight.bold,
                    color: BohoColors.marronOscuro,
                  ),
                ),
              ),
              IconButton(
                onPressed: _cancelarCaptura,
                icon: Icon(Icons.close),
                color: BohoColors.marronOscuro.withOpacity(0.6),
              ),
            ],
          ),
          
          SizedBox(height: 16),
          
          Text(
            'Después de \"${_formatearMicroaccion(_microaccionActual!.tipoMicroaccion)}\"',
            style: TextStyle(
              fontSize: 14,
              color: BohoColors.marronOscuro.withOpacity(0.7),
              fontStyle: FontStyle.italic,
            ),
          ),
          
          SizedBox(height: 24),
          
          // Sliders para capturar estado actual
          _buildMoodMapCapture(),
          
          SizedBox(height: 24),
          
          // Botón guardar
          SizedBox(
            width: double.infinity,
            child: ElevatedButton.icon(
              onPressed: _guardarSeguimiento,
              icon: Icon(Icons.check),
              label: Text('Registrar mi estado'),
              style: ElevatedButton.styleFrom(
                backgroundColor: BohoColors.verdeOliva,
                foregroundColor: Colors.white,
                padding: EdgeInsets.symmetric(vertical: 16),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(30),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildMoodMapCapture() {
    return StatefulBuilder(
      builder: (context, setSliderState) {
        double felicidad = 0.5;
        double estres = 0.5;
        double motivacion = 0.5;

        return Column(
          children: [
            _buildSlider(
              'Felicidad',
              felicidad,
              Icons.sentiment_very_satisfied,
              BohoColors.dorado,
              (value) => setSliderState(() => felicidad = value),
            ),
            SizedBox(height: 16),
            _buildSlider(
              'Estrés',
              estres,
              Icons.stress_management,
              BohoColors.terracota,
              (value) => setSliderState(() => estres = value),
            ),
            SizedBox(height: 16),
            _buildSlider(
              'Motivación',
              motivacion,
              Icons.rocket_launch,
              BohoColors.verdeOliva,
              (value) => setSliderState(() => motivacion = value),
            ),
          ],
        );
      },
    );
  }

  Widget _buildSlider(
    String label,
    double value,
    IconData icon,
    Color color,
    ValueChanged<double> onChanged,
  ) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          children: [
            Icon(icon, color: color, size: 20),
            SizedBox(width: 8),
            Text(
              label,
              style: TextStyle(
                fontSize: 16,
                fontWeight: FontWeight.w600,
                color: BohoColors.marronOscuro,
              ),
            ),
            Spacer(),
            Text(
              '${(value * 100).round()}%',
              style: TextStyle(
                fontSize: 14,
                color: color,
                fontWeight: FontWeight.bold,
              ),
            ),
          ],
        ),
        SizedBox(height: 8),
        SliderTheme(
          data: SliderTheme.of(context).copyWith(
            activeTrackColor: color.withOpacity(0.8),
            inactiveTrackColor: color.withOpacity(0.2),
            thumbColor: color,
            overlayColor: color.withOpacity(0.2),
          ),
          child: Slider(
            value: value,
            onChanged: onChanged,
            min: 0.0,
            max: 1.0,
          ),
        ),
      ],
    );
  }

  String _formatearTiempo(Duration duracion) {
    if (duracion.inHours > 0) {
      return '${duracion.inHours}h ${duracion.inMinutes % 60}min';
    }
    return '${duracion.inMinutes}min';
  }

  String _formatearMicroaccion(String microaccion) {
    final Map<String, String> etiquetas = {
      'respiracion': 'Respiración profunda',
      'caminata': 'Caminata',
      'meditacion': 'Meditación',
      'musica': 'Música relajante',
      'ejercicio': 'Ejercicio suave',
      'te_caliente': 'Té caliente',
      'gratitud': 'Escribir gratitud',
      'estiramientos': 'Estiramientos',
      'llamar_amigo': 'Llamar amigo',
      'lectura': 'Lectura',
      'arte_dibujo': 'Arte/Dibujo',
      'bano_relajante': 'Baño relajante',
    };
    
    return etiquetas[microaccion] ?? microaccion.replaceAll('_', ' ');
  }

  void _iniciarCaptura(MicroaccionPendiente recordatorio) {
    setState(() {
      _mostrandoCaptura = true;
      _microaccionActual = recordatorio;
    });
    _seguimientoService.marcarRecordatorioMostrado(recordatorio.id);
  }

  void _cancelarCaptura() {
    setState(() {
      _mostrandoCaptura = false;
      _microaccionActual = null;
    });
  }

  void _postponerRecordatorio(MicroaccionPendiente recordatorio) {
    // Mover recordatorio 5 minutos al futuro
    recordatorio.momentoRecordatorio.add(Duration(minutes: 5));
    _seguimientoService.marcarRecordatorioMostrado(recordatorio.id);
    
    setState(() {
      _recordatoriosPendientes.remove(recordatorio);
    });
    
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text('Te recordaremos en 5 minutos ⏰'),
        backgroundColor: BohoColors.verdeOliva,
      ),
    );
  }

  void _omitirRecordatorio(MicroaccionPendiente recordatorio) {
    _seguimientoService.marcarRecordatorioMostrado(recordatorio.id);
    
    setState(() {
      _recordatoriosPendientes.remove(recordatorio);
    });
    
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text('Recordatorio omitido'),
        backgroundColor: BohoColors.marronOscuro,
      ),
    );
  }

  void _guardarSeguimiento() async {
    if (_microaccionActual == null) return;

    // TODO: Obtener valores reales de los sliders
    final moodmapPosterior = MoodMapData(
      felicidad: 0.7, // Valor del slider
      estres: 0.3,    // Valor del slider  
      motivacion: 0.8, // Valor del slider
    );

    try {
      final resultado = await _seguimientoService.completarSeguimiento(
        usuarioId: widget.usuarioId,
        tipoMicroaccion: _microaccionActual!.tipoMicroaccion,
        moodmapPosterior: moodmapPosterior,
      );

      if (resultado['exito']) {
        // Notificar al widget padre
        widget.onMoodMapCapturado?.call(moodmapPosterior);
        
        // Mostrar resultado
        _mostrarResultadoEfectividad(resultado);
        
        setState(() {
          _mostrandoCaptura = false;
          _microaccionActual = null;
          _recordatoriosPendientes.clear();
        });
      } else {
        throw Exception(resultado['error']);
      }
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('Error al guardar: $e'),
          backgroundColor: Colors.red,
        ),
      );
    }
  }

  void _mostrarResultadoEfectividad(Map<String, dynamic> resultado) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
        title: Row(
          children: [
            Icon(Icons.analytics, color: BohoColors.verdeOliva),
            SizedBox(width: 8),
            Text('Efectividad'),
          ],
        ),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Text(
              'La microacción fue ${resultado["efectividad_objetiva"] > 0 ? "efectiva" : "poco efectiva"}',
              style: TextStyle(fontSize: 16),
            ),
            SizedBox(height: 16),
            ...resultado['mejoras'].entries.map<Widget>((entry) {
              final valor = entry.value as double;
              return Padding(
                padding: EdgeInsets.symmetric(vertical: 4),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Text(entry.key),
                    Text(
                      '${valor > 0 ? "+" : ""}${valor.toStringAsFixed(2)}',
                      style: TextStyle(
                        color: valor > 0 ? Colors.green : Colors.red,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ],
                ),
              );
            }).toList(),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(),
            child: Text('Entendido'),
          ),
        ],
      ),
    );
  }
}