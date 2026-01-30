import 'dart:convert';
import 'package:http/http.dart' as http;

/// Servicio para análisis emocional con IA/ML
class AnalisisEmocionService {
  static const String baseUrl = 'http://localhost:8000';

  /// Analiza el estado emocional actual y obtiene sugerencias de IA
  static Future<Map<String, dynamic>> analizarMoodMap({
    required double felicidad,
    required double estres,
    required double motivacion,
    required int usuarioId,
  }) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/moodmap/analizar'),
        headers: {
          'Content-Type': 'application/json',
        },
        body: jsonEncode({
          'felicidad': felicidad,
          'estres': estres,
          'motivacion': motivacion,
          'usuario_id': usuarioId,
        }),
      );

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        throw Exception('Error en análisis: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error de conexión: $e');
    }
  }

  /// Envía feedback de una actividad completada y recibe nuevo estado emocional
  static Future<Map<String, dynamic>> procesarFeedbackActividad({
    required String tipoActividad,
    required String nombreActividad,
    required int intensidad,
    required String? notas,
    required int usuarioId,
    required Map<String, double> estadoAnterior,
  }) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/feedback/procesar-actividad'),
        headers: {
          'Content-Type': 'application/json',
        },
        body: jsonEncode({
          'tipo_actividad': tipoActividad,
          'nombre_actividad': nombreActividad,
          'intensidad': intensidad,
          'notas': notas,
          'usuario_id': usuarioId,
          'estado_anterior': estadoAnterior,
          'timestamp': DateTime.now().toIso8601String(),
        }),
      );

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        throw Exception('Error en feedback: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error de conexión: $e');
    }
  }

  /// Obtiene sugerencias personalizadas basadas en patrones de comportamiento
  static Future<List<Map<String, dynamic>>> obtenerSugerenciasPersonalizadas({
    required int usuarioId,
    required Map<String, double> estadoEmocionalActual,
  }) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/ia/sugerencias-personalizadas'),
        headers: {
          'Content-Type': 'application/json',
        },
        body: jsonEncode({
          'usuario_id': usuarioId,
          'estado_actual': estadoEmocionalActual,
        }),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return List<Map<String, dynamic>>.from(data['sugerencias']);
      } else {
        throw Exception('Error en sugerencias: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error de conexión: $e');
    }
  }

  /// Calcula el impacto de una actividad en el estado emocional
  static Map<String, double> calcularImpactoActividad({
    required String tipoChemical,
    required int intensidad,
    required Map<String, double> estadoAnterior,
  }) {
    // Factores de impacto por tipo de chemical
    final Map<String, Map<String, double>> impactosPorChemical = {
      'serotonina': {
        'felicidad': 0.15,
        'estres': -0.10,
        'motivacion': 0.05,
      },
      'dopamina': {
        'felicidad': 0.10,
        'estres': -0.05,
        'motivacion': 0.20,
      },
      'endorfinas': {
        'felicidad': 0.12,
        'estres': -0.15,
        'motivacion': 0.08,
      },
      'oxitocina': {
        'felicidad': 0.18,
        'estres': -0.12,
        'motivacion': 0.10,
      },
    };

    final impactos = impactosPorChemical[tipoChemical] ?? {
      'felicidad': 0.05,
      'estres': -0.05,
      'motivacion': 0.05,
    };

    // Multiplicar por intensidad (normalizada)
    final factor = intensidad / 5.0;

    return {
      'felicidad': (estadoAnterior['felicidad']! + 
        (impactos['felicidad']! * factor)).clamp(0.0, 1.0),
      'estres': (estadoAnterior['estres']! + 
        (impactos['estres']! * factor)).clamp(0.0, 1.0),
      'motivacion': (estadoAnterior['motivacion']! + 
        (impactos['motivacion']! * factor)).clamp(0.0, 1.0),
    };
  }

  /// Genera sugerencias locales basadas en estado emocional
  static List<String> generarSugerenciasLocales({
    required double felicidad,
    required double estres,
    required double motivacion,
  }) {
    List<String> sugerencias = [];

    // Análisis de estrés
    if (estres > 0.7) {
      sugerencias.addAll(['endorfinas', 'serotonina']);
    }

    // Análisis de motivación
    if (motivacion < 0.4) {
      sugerencias.addAll(['dopamina', 'serotonina']);
    }

    // Análisis de felicidad
    if (felicidad < 0.5) {
      sugerencias.addAll(['serotonina', 'oxitocina']);
    }

    // Si todo está bien, mantener el estado
    if (felicidad > 0.7 && estres < 0.3 && motivacion > 0.7) {
      sugerencias.addAll(['oxitocina', 'dopamina']);
    }

    return sugerencias.toSet().toList(); // Eliminar duplicados
  }
}