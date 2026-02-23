"""
PERSONA 2 — ai/minimax.py
============================================================
Responsabilidad: Implementar el algoritmo Minimax con Alpha-Beta Pruning.

Estructura exacta que pide el profesor:
    - maximize(state, depth, alpha, beta)  → (child_state, utility)
    - minimize(state, depth, alpha, beta)  → (child_state, utility)
    - decision(state, depth)               → child_state

Dependencias:
    - ai/game_state.py  (Persona 1) → state.is_terminal(), state.eval(), state.children()

NO necesitas modificar ningún archivo de game/.
Tu trabajo es 100% el algoritmo.
============================================================
"""

from math import inf


def maximize(state, depth: int, alpha: float, beta: float) -> tuple:
    """
    Encuentra el estado hijo con el MAYOR valor de utilidad.
    Juega desde la perspectiva del jugador que quiere maximizar.

    Pseudocódigo del profesor (con alpha-beta y profundidad añadidos):

        function MAXIMIZE(state, depth, alpha, beta):
            if TERMINAL-TEST(state) or depth == 0:
                return (NULL, EVAL(state))

            maxChild, maxUtility = NULL, -∞

            for child in state.children():
                _, utility = MINIMIZE(child, depth-1, alpha, beta)

                if utility > maxUtility:
                    maxChild, maxUtility = child, utility

                alpha = max(alpha, maxUtility)
                if alpha >= beta:
                    break  ← Poda Beta: el minimizador nunca elegiría este camino

            return (maxChild, maxUtility)

    Args:
        state:  GameState actual.
        depth:  Profundidad restante. Cuando llega a 0, se evalúa con heurística.
        alpha:  Mejor valor garantizado para el maximizador hasta ahora (-∞ al inicio).
        beta:   Mejor valor garantizado para el minimizador hasta ahora (+∞ al inicio).

    Returns:
        tuple: (mejor_estado_hijo, utilidad)
               mejor_estado_hijo es None si el estado es terminal o sin hijos.
    """
    # TODO — Persona 2
    #
    # terminal, _ = state.is_terminal()
    # if terminal or depth == 0:
    #     return (None, state.eval())
    #
    # max_child, max_utility = None, -inf
    #
    # for child in state.children():
    #     _, utility = minimize(child, depth - 1, alpha, beta)
    #
    #     if utility > max_utility:
    #         max_child, max_utility = child, utility
    #
    #     alpha = max(alpha, max_utility)
    #     if alpha >= beta:
    #         break  # Poda beta
    #
    # return (max_child, max_utility)
    #
    raise NotImplementedError("Persona 2: implementar maximize()")


def minimize(state, depth: int, alpha: float, beta: float) -> tuple:
    """
    Encuentra el estado hijo con el MENOR valor de utilidad.
    Juega desde la perspectiva del jugador que quiere minimizar.

    Pseudocódigo del profesor (con alpha-beta y profundidad añadidos):

        function MINIMIZE(state, depth, alpha, beta):
            if TERMINAL-TEST(state) or depth == 0:
                return (NULL, EVAL(state))

            minChild, minUtility = NULL, +∞

            for child in state.children():
                _, utility = MAXIMIZE(child, depth-1, alpha, beta)

                if utility < minUtility:
                    minChild, minUtility = child, utility

                beta = min(beta, minUtility)
                if alpha >= beta:
                    break  ← Poda Alpha: el maximizador nunca elegiría este camino

            return (minChild, minUtility)

    Args:
        state:  GameState actual.
        depth:  Profundidad restante.
        alpha:  Mejor valor garantizado para el maximizador.
        beta:   Mejor valor garantizado para el minimizador.

    Returns:
        tuple: (peor_estado_hijo, utilidad)
    """
    # TODO — Persona 2
    #
    # terminal, _ = state.is_terminal()
    # if terminal or depth == 0:
    #     return (None, state.eval())
    #
    # min_child, min_utility = None, inf
    #
    # for child in state.children():
    #     _, utility = maximize(child, depth - 1, alpha, beta)
    #
    #     if utility < min_utility:
    #         min_child, min_utility = child, utility
    #
    #     beta = min(beta, min_utility)
    #     if alpha >= beta:
    #         break  # Poda alpha
    #
    # return (min_child, min_utility)
    #
    raise NotImplementedError("Persona 2: implementar minimize()")


def decision(state, depth: int) -> object:
    """
    Punto de entrada del Minimax. Retorna el MEJOR estado hijo.

    Equivale al DECISION del profesor:
        function DECISION(state):
            child, _ = MAXIMIZE(state)
            return child

    Args:
        state: GameState actual (estado raíz de la búsqueda).
        depth: Profundidad máxima permitida para esta llamada.

    Returns:
        GameState: El mejor estado hijo encontrado.
                   None si no hay movimientos disponibles.

    Nota para Persona 5 (IDS):
        IDS llama a esta función con depth=1, luego depth=2, etc.
        hasta que se agote el tiempo. Siempre guarda el último resultado.
    """
    # TODO — Persona 2
    #
    # child, _ = maximize(state, depth, -inf, inf)
    # return child
    #
    raise NotImplementedError("Persona 2: implementar decision()")
