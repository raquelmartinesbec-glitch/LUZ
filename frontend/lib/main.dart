import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:google_fonts/google_fonts.dart';
import 'screens/inicio_screen.dart';
import 'theme/tema_boho.dart';

void main() {
  runApp(
    const ProviderScope(
      child: LuzBienestarApp(),
    ),
  );
}

/// Aplicación principal de Luz - Bienestar Interactivo
/// Estilo: Boho chic zen con colores suaves y animaciones
class LuzBienestarApp extends StatelessWidget {
  const LuzBienestarApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Luz - Bienestar',
      debugShowCheckedModeBanner: false,
      theme: TemaBoho.obtenerTema(),
      home: const InicioScreen(),
    );
  }
}
