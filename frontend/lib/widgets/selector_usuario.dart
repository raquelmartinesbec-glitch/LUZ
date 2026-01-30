import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../providers/usuario_provider.dart';
import '../providers/analisis_ia_provider.dart';
import '../theme/tema_boho.dart';

/// Widget para seleccionar entre los usuarios ficticios
class SelectorUsuario extends ConsumerWidget {
  const SelectorUsuario({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final usuariosLista = ref.watch(usuariosListaProvider);
    final usuarioActual = ref.watch(usuarioActualProvider);

    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(20),
        boxShadow: TemaBoho.obtenerSombraRelieve(),
      ),
      child: DropdownButtonHideUnderline(
        child: DropdownButton(
          value: usuarioActual?.id,
          icon: const Icon(Icons.arrow_drop_down, color: TemaBoho.colorPrimario),
          isExpanded: true,
          style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                color: TemaBoho.colorTexto,
                fontWeight: FontWeight.w500,
              ),
          items: usuariosLista.map((usuario) {
            return DropdownMenuItem(
              value: usuario.id,
              child: Row(
                children: [
                  // Avatar circular
                  Container(
                    width: 40,
                    height: 40,
                    decoration: BoxDecoration(
                      shape: BoxShape.circle,
                      gradient: LinearGradient(
                        colors: [
                          TemaBoho.colorPrimario,
                          TemaBoho.colorSecundario,
                        ],
                      ),
                      boxShadow: [
                        BoxShadow(
                          color: TemaBoho.colorPrimario.withOpacity(0.3),
                          blurRadius: 8,
                          offset: const Offset(0, 2),
                        ),
                      ],
                    ),
                    child: Center(
                      child: Text(
                        usuario.nombre[0],
                        style: const TextStyle(
                          color: Colors.white,
                          fontWeight: FontWeight.bold,
                          fontSize: 18,
                        ),
                      ),
                    ),
                  ),
                  const SizedBox(width: 12),
                  // Nombre del usuario
                  Text(usuario.nombre),
                ],
              ),
            );
          }).toList(),
          onChanged: (int? nuevoId) {
            if (nuevoId != null) {
              final nuevoUsuario = usuariosLista.firstWhere(
                (u) => u.id == nuevoId,
              );
              ref.read(usuarioActualProvider.notifier).state = nuevoUsuario;
              
              // Actualizar también el moodmap y alma board tradicionales
              ref.read(moodmapProvider.notifier).state = nuevoUsuario.moodmap;
              ref.read(almaBoardProvider.notifier).state = nuevoUsuario.almaBoard;
              ref.read(microaccionesProvider.notifier).state = nuevoUsuario.microacciones;
              ref.read(destellosProvider.notifier).state = nuevoUsuario.destellos;
              
              // Actualizar MoodMap con IA
              ref.read(moodmapConIAProvider.notifier).establecerUsuario(nuevoUsuario);
            }
          },
        ),
      ),
    );
  }
}
