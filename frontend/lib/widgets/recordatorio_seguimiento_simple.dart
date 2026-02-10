import 'package:flutter/material.dart';
import '../services/seguimiento_microacciones_service.dart';
import '../models/usuario_model.dart';
import '../theme/tema_boho.dart';

/// Widget simple para recordatorios de seguimiento post-microacción
class RecordatorioSeguimientoWidget extends StatefulWidget {
  final String usuarioId;

  const RecordatorioSeguimientoWidget({
    Key? key,
    required this.usuarioId,
  }) : super(key: key);

  @override
  State<RecordatorioSeguimientoWidget> createState() => _RecordatorioSeguimientoWidgetState();
}

class _RecordatorioSeguimientoWidgetState extends State<RecordatorioSeguimientoWidget> {
  final SeguimientoMicroaccionesService _seguimientoService = SeguimientoMicroaccionesService();
  List<MicroaccionPendiente> _recordatoriosPendientes = [];

  @override
  void initState() {
    super.initState();
    _verificarRecordatorios();
  }

  void _verificarRecordatorios() {
    final pendientes = _seguimientoService.obtenerRecordatoriosPendientes()
        .where((m) => m.usuarioId == widget.usuarioId)
        .toList();

    setState(() {
      _recordatoriosPendientes = pendientes;
    });
  }

  @override
  Widget build(BuildContext context) {
    if (_recordatoriosPendientes.isEmpty) {
      return SizedBox.shrink();
    }

    return Card(
      margin: EdgeInsets.all(16),
      child: Padding(
        padding: EdgeInsets.all(20),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Row(
              children: [
                Icon(Icons.schedule, color: TemaBoho.colorPrimario),
                SizedBox(width: 12),
                Expanded(
                  child: Text(
                    '¡Hora de seguimiento!',
                    style: TextStyle(
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                      color: TemaBoho.colorTexto,
                    ),
                  ),
                ),
              ],
            ),
            SizedBox(height: 12),
            Text(
              'Te recordamos verificar cómo te sientes después de la microacción',
              style: TextStyle(
                color: TemaBoho.colorTexto.withOpacity(0.8),
              ),
            ),
            SizedBox(height: 16),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [
                OutlinedButton(
                  onPressed: _omitirRecordatorio,
                  child: Text('Omitir'),
                ),
                ElevatedButton(
                  onPressed: _mostrarCaptura,
                  style: ElevatedButton.styleFrom(
                    backgroundColor: TemaBoho.colorPrimario,
                  ),
                  child: Text('¿Cómo estoy?'),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  void _omitirRecordatorio() {
    setState(() {
      _recordatoriosPendientes.clear();
    });
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text('Recordatorio omitido')),
    );
  }

  void _mostrarCaptura() {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text('¿Cómo te sientes?'),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Text('Funcionalidad de captura de estado emocional'),
            SizedBox(height: 20),
            Text('(Por implementar en siguiente versión)'),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(),
            child: Text('Cerrar'),
          ),
        ],
      ),
    );
  }
}