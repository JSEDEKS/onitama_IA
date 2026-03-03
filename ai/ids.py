

import time
from ai.minimax import minimax


# Profundidad máxima absoluta (protección contra búsqueda infinita)
MAX_DEPTH = 20


def ids_decision(state, max_time: float = 3.0, heuristics_count=5, weights=None) -> tuple:
  
    start_time = time.time()

    best_child = None
    depth_reached = 0
    nodes_expanded = 0

    for depth in range(1, MAX_DEPTH + 1):
        elapsed = time.time() - start_time
        if elapsed >= max_time:
            break

        # Adaptador para usar la clase minimax
        player_name = state.current_player.name
        agent = minimax(
            player_name, 
            max_depth=depth,
            heuristics_count=heuristics_count,
            weights=weights
        )
        best_move = agent.solve(state)

        # Convertir el movimiento (tuple) al estado hijo correspondiente
        current_result = None
        if best_move:
            for child in state.children():
                if child.last_move == best_move:
                    current_result = child
                    break

        # Solo actualizar si terminamos la búsqueda a tiempo
        elapsed_after = time.time() - start_time
        if elapsed_after < max_time:
            best_child = current_result
            depth_reached = depth
        else:
            # Si se acabó el tiempo durante la búsqueda, descartamos este nivel
            break

        # Si el estado es terminal, no hay más profundidad que explorar
        if state.is_terminal():
            break

    time_used = time.time() - start_time

    metrics = {
        "nodes_expanded": nodes_expanded,
        "depth_reached":  depth_reached,
        "time_used":      round(time_used, 4)
    }

    return (best_child, metrics)


if __name__ == "__main__":
    print("\n⚠️  ADVERTENCIA: Este archivo es una librería, no un ejecutable.")
    print("   Por favor, ejecuta el juego usando: python main.py --benchmark\n")