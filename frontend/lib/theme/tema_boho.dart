import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

/// Tema visual boho chic zen con colores suaves, degradados y sombras
class TemaBoho {
  // Colores base - Paleta boho chic zen
  static const Color colorPrimario = Color(0xFFD4A59A); // Rosa suave
  static const Color colorSecundario = Color(0xFFA8DADC); // Azul pastel
  static const Color colorTerciario = Color(0xFFE9C46A); // Amarillo suave
  static const Color colorFondo = Color(0xFFFAF3F0); // Beige claro
  static const Color colorTexto = Color(0xFF5D4E4A); // Marrón oscuro
  static const Color colorAcento = Color(0xFFB8A99A); // Taupe
  
  // Colores emocionales
  static const Color colorFelicidad = Color(0xFFFFA07A); // Coral claro
  static const Color colorEstres = Color(0xFF9370DB); // Violeta medio
  static const Color colorMotivacion = Color(0xFF98D8C8); // Verde menta
  static const Color colorCalma = Color(0xFFAEC6CF); // Azul pastel
  static const Color colorTristeza = Color(0xFFB0C4DE); // Azul acero claro
  
  /// Obtiene el tema completo de la aplicación
  static ThemeData obtenerTema() {
    return ThemeData(
      useMaterial3: true,
      colorScheme: ColorScheme.light(
        primary: colorPrimario,
        secondary: colorSecundario,
        tertiary: colorTerciario,
        surface: colorFondo,
        onPrimary: Colors.white,
        onSecondary: colorTexto,
        onSurface: colorTexto,
      ),
      
      // Tipografía con Google Fonts - estilo boho
      textTheme: TextTheme(
        displayLarge: GoogleFonts.cormorant(
          fontSize: 36,
          fontWeight: FontWeight.w300,
          color: colorTexto,
          letterSpacing: 1.2,
        ),
        displayMedium: GoogleFonts.cormorant(
          fontSize: 28,
          fontWeight: FontWeight.w400,
          color: colorTexto,
        ),
        headlineMedium: GoogleFonts.montserrat(
          fontSize: 24,
          fontWeight: FontWeight.w500,
          color: colorTexto,
        ),
        titleLarge: GoogleFonts.montserrat(
          fontSize: 20,
          fontWeight: FontWeight.w600,
          color: colorTexto,
        ),
        bodyLarge: GoogleFonts.lato(
          fontSize: 16,
          fontWeight: FontWeight.w400,
          color: colorTexto,
        ),
        bodyMedium: GoogleFonts.lato(
          fontSize: 14,
          color: colorTexto,
        ),
        labelLarge: GoogleFonts.montserrat(
          fontSize: 16,
          fontWeight: FontWeight.w500,
          color: Colors.white,
        ),
      ),
      
      // Elevación y sombras
      cardTheme: CardThemeData(
        elevation: 8,
        shadowColor: Colors.black26,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(20),
        ),
        color: Colors.white,
      ),
      
      // Botones con sombras y relieve
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          elevation: 6,
          shadowColor: Colors.black26,
          padding: const EdgeInsets.symmetric(horizontal: 32, vertical: 16),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(25),
          ),
        ),
      ),
      
      // AppBar con degradado
      appBarTheme: AppBarTheme(
        elevation: 0,
        centerTitle: true,
        backgroundColor: colorPrimario,
        foregroundColor: Colors.white,
        titleTextStyle: GoogleFonts.cormorant(
          fontSize: 24,
          fontWeight: FontWeight.w500,
          color: Colors.white,
        ),
      ),
      
      // Input decoration
      inputDecorationTheme: InputDecorationTheme(
        filled: true,
        fillColor: Colors.white,
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(15),
          borderSide: BorderSide(color: colorAcento, width: 1),
        ),
        enabledBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(15),
          borderSide: BorderSide(color: colorAcento.withOpacity(0.5), width: 1),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(15),
          borderSide: BorderSide(color: colorPrimario, width: 2),
        ),
        contentPadding: const EdgeInsets.symmetric(horizontal: 20, vertical: 16),
      ),
      
      // Sliders con estilo boho
      sliderTheme: SliderThemeData(
        activeTrackColor: colorPrimario,
        inactiveTrackColor: colorAcento.withOpacity(0.3),
        thumbColor: colorPrimario,
        overlayColor: colorPrimario.withOpacity(0.2),
        trackHeight: 6,
      ),
    );
  }
  
  /// Obtiene un degradado boho para fondos
  static LinearGradient obtenerDegradadoFondo() {
    return const LinearGradient(
      begin: Alignment.topLeft,
      end: Alignment.bottomRight,
      colors: [
        Color(0xFFFAF3F0),
        Color(0xFFFFE8E0),
        Color(0xFFF5E6E8),
      ],
    );
  }
  
  /// Obtiene una sombra suave para elementos con relieve
  static List<BoxShadow> obtenerSombraRelieve() {
    return [
      BoxShadow(
        color: Colors.black.withOpacity(0.1),
        blurRadius: 20,
        offset: const Offset(0, 10),
        spreadRadius: -5,
      ),
      BoxShadow(
        color: Colors.white.withOpacity(0.7),
        blurRadius: 10,
        offset: const Offset(-5, -5),
      ),
    ];
  }
  
  /// Obtiene sombra difusa para destellos de luz
  static List<BoxShadow> obtenerSombraDestello(Color color) {
    return [
      BoxShadow(
        color: color.withOpacity(0.6),
        blurRadius: 30,
        spreadRadius: 5,
      ),
      BoxShadow(
        color: color.withOpacity(0.3),
        blurRadius: 50,
        spreadRadius: 10,
      ),
    ];
  }
}
