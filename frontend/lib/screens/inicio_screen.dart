import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../theme/tema_boho.dart';
import '../providers/usuario_provider.dart';
import 'moodmap_screen.dart';
import 'alma_board_screen.dart';
import '../widgets/selector_usuario.dart';

/// Pantalla de inicio con navegación principal
/// Presenta el MoodMap Board y Alma Board
class InicioScreen extends ConsumerStatefulWidget {
  const InicioScreen({super.key});

  @override
  ConsumerState<InicioScreen> createState() => _InicioScreenState();
}

class _InicioScreenState extends ConsumerState<InicioScreen>
    with SingleTickerProviderStateMixin {
  late TabController _tabController;

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 2, vsync: this);
  }

  @override
  void dispose() {
    _tabController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final usuarioActual = ref.watch(usuarioActualProvider);

    return Scaffold(
      // Fondo con degradado boho
      body: Container(
        decoration: BoxDecoration(
          gradient: TemaBoho.obtenerDegradadoFondo(),
        ),
        child: SafeArea(
          child: Column(
            children: [
              // Header con selector de usuario
              _construirHeader(usuarioActual),

              // Tabs para navegar entre MoodMap y Alma Board
              _construirTabs(),

              // Contenido de las tabs
              Expanded(
                child: TabBarView(
                  controller: _tabController,
                  children: const [
                    MoodMapScreen(),
                    AlmaBoardScreen(),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  /// Construye el header con información del usuario
  Widget _construirHeader(dynamic usuarioActual) {
    return Container(
      padding: const EdgeInsets.all(20),
      child: Column(
        children: [
          // Logo y título
          Text(
            'Luz',
            style: Theme.of(context).textTheme.displayLarge?.copyWith(
                  color: TemaBoho.colorPrimario,
                  fontSize: 42,
                  fontWeight: FontWeight.w300,
                  letterSpacing: 2,
                ),
          ),
          const SizedBox(height: 4),
          Text(
            'Tu espacio de bienestar',
            style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                  color: TemaBoho.colorTexto.withOpacity(0.7),
                  fontSize: 14,
                  letterSpacing: 1.5,
                ),
          ),
          const SizedBox(height: 20),

          // Selector de usuario
          const SelectorUsuario(),
        ],
      ),
    );
  }

  /// Construye las tabs de navegación
  Widget _construirTabs() {
    return Container(
      margin: const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(25),
        boxShadow: TemaBoho.obtenerSombraRelieve(),
      ),
      child: TabBar(
        controller: _tabController,
        indicator: BoxDecoration(
          gradient: LinearGradient(
            colors: [
              TemaBoho.colorPrimario,
              TemaBoho.colorSecundario,
            ],
          ),
          borderRadius: BorderRadius.circular(25),
          boxShadow: [
            BoxShadow(
              color: TemaBoho.colorPrimario.withOpacity(0.3),
              blurRadius: 8,
              offset: const Offset(0, 4),
            ),
          ],
        ),
        labelColor: Colors.white,
        unselectedLabelColor: TemaBoho.colorTexto.withOpacity(0.6),
        labelStyle: const TextStyle(
          fontSize: 16,
          fontWeight: FontWeight.w600,
          letterSpacing: 0.5,
        ),
        tabs: const [
          Tab(
            icon: Icon(Icons.mood),
            text: 'MoodMap',
          ),
          Tab(
            icon: Icon(Icons.self_improvement),
            text: 'Alma Board',
          ),
        ],
      ),
    );
  }
}
