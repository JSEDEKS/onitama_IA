"""
PERSONA 4 — ai/ai_player.py
============================================================
Responsabilidad: Implementar los agentes (jugadores) de IA.

Todos los agentes heredan de BaseAgent e implementan choose_move().
choose_move() recibe un GameState y retorna el GameState resultante
del movimiento elegido.

Tipos de agentes:
    RandomAgent   → movimiento al azar
    GreedyAgent   → mejor movimiento a profundidad 1
    WorstAgent    → peor movimiento posible (para benchmark)
    MinimaxAgent  → Minimax + Alpha-Beta + IDS (el agente principal)

Además, esta persona modifica:
    - game/player.py      → agregar atributo is_ai y agent
    - game/game_manager.py → integrar agentes en el game loop

Dependencias:
    - ai/game_state.py (Persona 1)
    - ai/minimax.py    (Persona 2) → decision()
    - ai/ids.py        (Persona 5) → ids_decision()
============================================================
"""

import random
from math import inf

from ai.game_state import GameState
from ai.minimax import decision, minimize
from ai.ids import ids_decision
from ai.heuristics import DEFAULT_WEIGHTS


# ── Clase base ────────────────────────────────────────────────────────────────

class BaseAgent:
    """
    Interfaz común para todos los agentes. NO modificar.

    Todos los agentes DEBEN heredar de esta clase e implementar choose_move().
    """

    def choose_move(self, state: GameState) -> GameState:
        """
        Elige el siguiente movimiento y retorna el estado resultante.

        Args:
            state: GameState actual (estado raíz para tomar la decisión).

        Returns:
            GameState: Estado resultante del movimiento elegido.
                       state.last_move contiene (card, piece, destination)
                       que game_manager usa para ejecutar el movimiento real.
            None: Si no hay movimientos disponibles (no debería ocurrir en Onitama).
        """
        raise NotImplementedError("Cada agente debe implementar choose_move()")


# ── Agentes concretos ─────────────────────────────────────────────────────────

class RandomAgent(BaseAgent):
    """
    Elige un movimiento completamente al azar entre todos los válidos.
    Usado en benchmark como oponente de referencia más simple.
    """

    def choose_move(self, state: GameState) -> GameState:
        """
        Genera todos los hijos y elige uno al azar.
        """
        # TODO — Persona 4
        #
        # children = state.children()
        # if not children:
        #     return None
        # return random.choice(children)
        #
        raise NotImplementedError("Persona 4: implementar RandomAgent.choose_move()")


class GreedyAgent(BaseAgent):
    """
    Elige el movimiento con el mejor valor heurístico inmediato (depth=1).
    No piensa en el futuro — solo en el siguiente paso.
    Usado en benchmark como oponente de referencia intermedio.
    """

    def choose_move(self, state: GameState) -> GameState:
        """
        Equivale a Minimax con profundidad 1 (solo maximizar, sin minimizar).
        """
        # TODO — Persona 4
        #
        # return decision(state, depth=1)
        #
        raise NotImplementedError("Persona 4: implementar GreedyAgent.choose_move()")


class WorstAgent(BaseAgent):
    """
    Siempre elige el PEOR movimiento posible.
    Útil para verificar que el MinimaxAgent siempre gana contra él.
    """

    def choose_move(self, state: GameState) -> GameState:
        """
        Usa minimize() en vez de maximize() para elegir el peor movimiento.
        """
        # TODO — Persona 4
        #
        # Tip: minimize() retorna el estado con MENOR utilidad (el peor para el jugador).
        # worst_child, _ = minimize(state, depth=1, alpha=-inf, beta=inf)
        # return worst_child
        #
        raise NotImplementedError("Persona 4: implementar WorstAgent.choose_move()")


class MinimaxAgent(BaseAgent):
    """
    Agente principal: Minimax + Alpha-Beta Pruning + IDS.

    Configurable para los distintos escenarios del benchmark:
        - max_time:         Tiempo máximo de búsqueda (1s, 3s, 10s).
        - heuristics_count: Cuántas heurísticas usar (1 a 5).
        - weights:          Pesos de las heurísticas (DEFAULT_WEIGHTS o ALT_WEIGHTS).
    """

    def __init__(
        self,
        max_time: float = 3.0,
        heuristics_count: int = 5,
        weights: list = None
    ):
        """
        Args:
            max_time:          Segundos máximos para buscar (default 3s).
            heuristics_count:  Número de heurísticas activas (1-5, default 5).
            weights:           Pesos personalizados. None = DEFAULT_WEIGHTS.
        """
        self.max_time = max_time
        self.heuristics_count = heuristics_count
        self.weights = weights if weights is not None else DEFAULT_WEIGHTS

        # Métricas de la última jugada (las lee Persona 5 para el benchmark)
        self.last_nodes_expanded = 0
        self.last_depth_reached  = 0
        self.last_time_used      = 0.0

    def choose_move(self, state: GameState) -> GameState:
        """
        Ejecuta IDS y retorna el mejor estado hijo encontrado.
        Actualiza las métricas internas para que Persona 5 pueda leerlas.
        """
        # TODO — Persona 4
        #
        # Nota: ids_decision necesita que el GameState use la configuración
        # de heurísticas correcta. Una forma simple: guardar la config en el
        # estado o pasarla como parámetro adicional.
        #
        # best_child, metrics = ids_decision(state, self.max_time)
        #
        # # Guardar métricas para el benchmark
        # self.last_nodes_expanded = metrics["nodes_expanded"]
        # self.last_depth_reached  = metrics["depth_reached"]
        # self.last_time_used      = metrics["time_used"]
        #
        # return best_child
        #
        raise NotImplementedError("Persona 4: implementar MinimaxAgent.choose_move()")