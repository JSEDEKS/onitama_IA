"""
PERSONA 5 — ai/ids.py
============================================================
Responsabilidad: Iterative Deepening Search (IDS) sobre el Minimax.

IDS ejecuta el Minimax con profundidad 1, luego 2, luego 3...
hasta que se acabe el tiempo. Siempre guarda el mejor resultado
encontrado antes de que el tiempo expire.

Por qué IDS y no profundidad fija:
    - Con tiempo fijo no sabemos qué profundidad alcanzaremos.
    - IDS garantiza que siempre tenemos una respuesta válida.
    - Si el tiempo se acaba en depth=4, usamos la respuesta de depth=3.

Dependencias:
    - ai/minimax.py  (Persona 2) → decision(state, depth)
    - ai/game_state.py (Persona 1) → GameState

NO necesitas modificar ningún archivo de game/.
============================================================
"""

import time
from ai.minimax import minimax


# Profundidad máxima absoluta (protección contra búsqueda infinita)
MAX_DEPTH = 20


def ids_decision(state, max_time: float = 3.0, heuristics_count=5, weights=None) -> tuple:
    """
    Ejecuta Minimax con profundidad creciente hasta agotar el tiempo.

    Algoritmo:
        best_result = decision(state, depth=1)
        for depth in 2, 3, 4, ..., MAX_DEPTH:
            if tiempo_restante <= 0: break
            resultado = decision(state, depth)
            best_result = resultado   ← sobreescribir solo si terminó a tiempo
        return best_result

    Args:
        state:     GameState raíz desde donde buscar.
        max_time:  Tiempo máximo en segundos (1.0, 3.0 o 10.0 para benchmark).
        heuristics_count: Cantidad de heurísticas a usar.
        weights:   Pesos personalizados.

    Returns:
        tuple: (best_child_state, metrics) donde metrics es un dict con:
            {
                "nodes_expanded":  int   — nodos visitados en la última iteración,
                "depth_reached":   int   — profundidad máxima completada,
                "time_used":       float — tiempo real usado en segundos
            }

    Nota: best_child_state puede ser None si el estado inicial es terminal.
    """
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