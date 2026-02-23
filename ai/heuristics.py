"""
PERSONA 3 — ai/heuristics.py
============================================================
Responsabilidad: Implementar las 5 funciones heurísticas de evaluación.

Estas funciones son llamadas por GameState.eval() (Persona 1).
Cada función recibe un estado y un jugador, y retorna un float.

Convención de signo (CRÍTICO — no cambiar):
    Valor POSITIVO → favorable para `player`
    Valor NEGATIVO → favorable para el oponente de `player`

Archivos de game/ que debes leer y entender:
    - game/board.py   → board.grid, board.get_enemy_temple()
    - game/pieces.py  → piece.position, piece.type ("MASTER" / "STUDENT")
    - game/rules.py   → para entender las condiciones de victoria

Coordinación con Persona 1:
    GameState.eval() llama: evaluate(state, state.current_player)
    Asegúrate de que la firma de evaluate() no cambie.
============================================================
"""

# ── Pesos por defecto ─────────────────────────────────────────────────────────
# Orden: [piece_count, master_safety, mobility, master_threat, temple_proximity]
# Persona 3 puede ajustar estos valores para el benchmark de configuraciones.
DEFAULT_WEIGHTS = [1.0, 1.5, 0.5, 2.0, 1.2]

# Segunda configuración de pesos (para comparativa en benchmark — Persona 5)
ALT_WEIGHTS = [2.0, 1.0, 1.0, 1.5, 0.5]


# ── Heurísticas individuales ──────────────────────────────────────────────────

def piece_count(state, player) -> float:
    """
    Heurística 1: Diferencia en cantidad de piezas.

    Más piezas propias y menos del oponente es mejor.
    Fórmula: len(player.pieces) - len(opponent.pieces)

    Rango típico: [-5, +5]
    """
    # TODO — Persona 3
    #
    # opponent = state.opponent if state.current_player == player else state.current_player
    # return float(len(player.pieces) - len(opponent.pieces))
    #
    raise NotImplementedError("Persona 3: implementar piece_count()")


def master_safety(state, player) -> float:
    """
    Heurística 2: Seguridad del maestro propio.

    Qué tan lejos está el maestro del jugador del templo enemigo.
    Cerca del templo enemigo = mejor (posición de ataque).
    Fórmula: 8 - distancia_manhattan(mi_maestro, templo_enemigo)

    Distancia máxima en un tablero 5x5: 8 pasos (0,0) → (4,4)
    Penalización si el maestro no existe: -100.0

    Rango típico: [0, +8]
    """
    # TODO — Persona 3
    #
    # master = player.get_master()
    # if master is None:
    #     return -100.0  # Maestro capturado → estado terrible
    # temple = state.board.get_enemy_temple(player)
    # dist = abs(master.position[0] - temple[0]) + abs(master.position[1] - temple[1])
    # return float(8 - dist)
    #
    raise NotImplementedError("Persona 3: implementar master_safety()")


def mobility(state, player) -> float:
    """
    Heurística 3: Cantidad de movimientos disponibles.

    Más opciones de movimiento = mayor flexibilidad táctica.
    Cuenta el total de destinos válidos sumando ambas cartas del jugador.

    Rango típico: [0, ~20]
    """
    # TODO — Persona 3
    #
    # total = 0
    # for card in player.cards:
    #     pieces_with_moves = state.card_manager.get_all_valid_moves(
    #         card, player, state.board
    #     )
    #     for destinations in pieces_with_moves.values():
    #         total += len(destinations)
    # return float(total)
    #
    raise NotImplementedError("Persona 3: implementar mobility()")


def master_threat(state, player) -> float:
    """
    Heurística 4: ¿Puede el jugador capturar al maestro enemigo?

    Verifica si algún movimiento válido de `player` alcanza la posición
    del maestro enemigo. Si puede capturarlo → gran ventaja.

    Valores:
        +10.0 → hay amenaza directa al maestro enemigo
          0.0 → no hay amenaza directa
        +100.0 → maestro enemigo ya fue capturado (estado casi terminal)
    """
    # TODO — Persona 3
    #
    # opponent = state.opponent if state.current_player == player else state.current_player
    # enemy_master = opponent.get_master()
    #
    # if enemy_master is None:
    #     return 100.0  # Maestro ya capturado
    #
    # enemy_master_pos = enemy_master.position
    #
    # for card in player.cards:
    #     pieces_with_moves = state.card_manager.get_all_valid_moves(
    #         card, player, state.board
    #     )
    #     for destinations in pieces_with_moves.values():
    #         if enemy_master_pos in destinations:
    #             return 10.0
    #
    # return 0.0
    #
    raise NotImplementedError("Persona 3: implementar master_threat()")


def temple_proximity(state, player) -> float:
    """
    Heurística 5: Proximidad del maestro propio al templo enemigo.

    Escala normalizada entre 0.0 y 4.0.
    Complementa a master_safety con un rango diferente para
    que el benchmark pueda comparar configuraciones distintas.

    Fórmula: max(0, 4 - distancia_manhattan(mi_maestro, templo_enemigo))
    Penalización si el maestro no existe: 0.0

    Rango: [0.0, +4.0]
    """
    # TODO — Persona 3
    #
    # master = player.get_master()
    # if master is None:
    #     return 0.0
    # temple = state.board.get_enemy_temple(player)
    # dist = abs(master.position[0] - temple[0]) + abs(master.position[1] - temple[1])
    # return float(max(0, 4 - dist))
    #
    raise NotImplementedError("Persona 3: implementar temple_proximity()")


# ── Función principal (llamada por GameState.eval()) ──────────────────────────

def evaluate(state, player, heuristics_count: int = 5, weights: list = None) -> float:
    """
    Combina las heurísticas activas en un único valor de evaluación.

    Esta es la función que llama GameState.eval(). NO cambiar la firma.

    Args:
        state:             GameState a evaluar.
        player:            Jugador desde cuya perspectiva se evalúa.
        heuristics_count:  Cuántas heurísticas usar (1 a 5).
                           Sirve para el benchmark que compara 1, 2, 3, 4 y 5 heurísticas.
        weights:           Lista de 5 pesos. None = DEFAULT_WEIGHTS.

    Returns:
        float: Valor heurístico combinado. Positivo = bueno para `player`.

    Ejemplo de uso desde GameState.eval():
        from ai.heuristics import evaluate
        return evaluate(self, self.current_player)
    """
    if weights is None:
        weights = DEFAULT_WEIGHTS

    # Lista de heurísticas en orden fijo — NO reordenar
    all_heuristics = [
        piece_count,       # Heurística 1
        master_safety,     # Heurística 2
        mobility,          # Heurística 3
        master_threat,     # Heurística 4
        temple_proximity,  # Heurística 5
    ]

    active_heuristics = all_heuristics[:heuristics_count]
    active_weights    = weights[:heuristics_count]

    total = 0.0
    for h_func, w in zip(active_heuristics, active_weights):
        total += w * h_func(state, player)

    return total
