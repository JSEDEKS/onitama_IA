"""
PERSONA 5 — ai/benchmark.py
============================================================
Responsabilidad: Sistema de benchmarking automatizado.

Ejecuta partidas automáticas entre agentes y recopila métricas
para los análisis que pide el profesor:

    A. MinimaxAgent vs RandomAgent
    B. MinimaxAgent vs GreedyAgent
    C. MinimaxAgent vs WorstAgent
    D. MinimaxAgent (config 1) vs MinimaxAgent (config 2)  ← pesos distintos
    E. MinimaxAgent vs MinimaxAgent (misma config)
    F. MinimaxAgent con 1, 2, 3, 4, 5 heurísticas
    G. MinimaxAgent con max_time = 1s, 3s, 10s

Métricas recopiladas por partida:
    - Ganador
    - Nodos expandidos
    - Profundidad máxima alcanzada
    - Tiempo de ejecución

Dependencias:
    - ai/game_state.py  (Persona 1)
    - ai/ai_player.py   (Persona 4)
    - ai/ids.py         (Persona 5)
    - game/board.py, game/player.py, game/cards.py, game/rules.py
============================================================
"""

import time

from game.board import Board
from game.player import Player
from game.cards import CardManager
from game.rules import Rules
from ai.game_state import GameState
from ai.ai_player import RandomPlayer, GreedyPlayer, MinimaxPlayer
from ai.heuristics import Heuristics

# Máximo de turnos por partida para evitar partidas infinitas
MAX_TURNS = 200


# ── Auxiliares ────────────────────────────────────────────────────────────────

def _find_real_piece(player, position):
    """
    Busca en el jugador real la pieza que está en `position`.

    Necesario porque last_move guarda referencias al estado copiado (deepcopy),
    no al juego real. Se busca por posición porque es única en el tablero.

    Args:
        player:   Objeto Player del juego real.
        position: Tupla (x, y) de la posición a buscar.

    Returns:
        Piece si se encuentra, None si no.
    """
    for piece in player.pieces:
        if piece.position == position:
            return piece
    return None


def _find_real_card(player, card_name):
    """
    Busca en el jugador real la carta con el nombre dado.

    Args:
        player:    Objeto Player del juego real.
        card_name: Nombre de la carta (ej. "Tiger", "Dragon").

    Returns:
        Card si se encuentra, None si no.
    """
    for card in player.cards:
        if card.name == card_name:
            return card
    return None


# ── Motor de partida silenciosa (sin UI) ─────────────────────────────────────

def run_match(agent1: BaseAgent, agent2: BaseAgent) -> dict:
    """
    Ejecuta una partida completa entre dos agentes sin mostrar nada en pantalla.

    agent1 juega como RED  (jugador 0, índice 0)
    agent2 juega como BLUE (jugador 1, índice 1)

    La partida termina cuando:
        - Un agente gana (is_terminal retorna True)
        - Se alcanzan MAX_TURNS turnos → empate

    Args:
        agent1: Agente que controla a RED.
        agent2: Agente que controla a BLUE.

    Returns:
        dict:
        {
            "winner":         "RED" | "BLUE" | "DRAW",
            "turns":          int,
            "nodes_expanded": int,
            "depth_reached":  int,
            "time_used":      float (segundos)
        }
    """
    # ── Inicializar juego ─────────────────────────────────────────────────────
    board        = Board()
    players      = [Player("RED", "RED"), Player("BLUE", "BLUE")]
    card_manager = CardManager()
    rules        = Rules()

    board.setup(players)
    card_manager.deal_cards(players)

    agents = [agent1, agent2]

    # ── Métricas acumuladas ───────────────────────────────────────────────────
    start_time     = time.time()
    total_nodes    = 0
    max_depth      = 0
    current_index  = 0  # 0 = RED, 1 = BLUE

    # ── Loop de la partida ────────────────────────────────────────────────────
    for turn in range(MAX_TURNS):

        # Construir GameState desde el estado real actual
        state = GameState.from_game(board, players, card_manager, current_index)

        # Verificar si ya hay ganador (el movimiento anterior fue decisivo)
        terminal, winner = state.is_terminal()
        if terminal:
            return {
                "winner":         winner.color if winner else "DRAW",
                "turns":          turn,
                "nodes_expanded": total_nodes,
                "depth_reached":  max_depth,
                "time_used":      round(time.time() - start_time, 4)
            }

        # Pedir al agente su movimiento
        next_state = agents[current_index].choose_move(state)

        # Recopilar métricas del agente si es MinimaxAgent
        agent = agents[current_index]
        if hasattr(agent, "last_nodes_expanded"):
            total_nodes += agent.last_nodes_expanded
        if hasattr(agent, "last_depth_reached"):
            max_depth = max(max_depth, agent.last_depth_reached)

        # Caso sin movimientos: swap de carta y pasar turno
        if next_state is None or next_state.last_move is None:
            real_card = players[current_index].cards[0]
            card_manager.swap_card(players[current_index], real_card)
            current_index = 1 - current_index
            continue

        # Extraer el movimiento del estado copiado
        ai_card, ai_piece, destination = next_state.last_move

        # Traducir a objetos reales del juego
        real_piece = _find_real_piece(players[current_index], ai_piece.position)
        real_card  = _find_real_card(players[current_index], ai_card.name)

        if real_piece is None or real_card is None:
            break

        # Aplicar el movimiento en el juego real
        board.move_piece(real_piece.position, destination)
        card_manager.swap_card(players[current_index], real_card)

        current_index = 1 - current_index

    # Si se agotaron los turnos → empate
    return {
        "winner":         "DRAW",
        "turns":          MAX_TURNS,
        "nodes_expanded": total_nodes,
        "depth_reached":  max_depth,
        "time_used":      round(time.time() - start_time, 4)
    }


# ── Suite de benchmarks ───────────────────────────────────────────────────────

def run_benchmark(agent1: BaseAgent, agent2: BaseAgent, num_games: int = 10) -> list:
    """
    Ejecuta múltiples partidas entre dos agentes y retorna los resultados.

    Args:
        agent1:    Primer agente (RED).
        agent2:    Segundo agente (BLUE).
        num_games: Número de partidas a jugar.

    Returns:
        list[dict]: Lista de resultados, uno por partida.
    """
    results = []
    for i in range(num_games):
        print(f"  Partida {i + 1}/{num_games}...", end="\r")
        result = run_match(agent1, agent2)
        results.append(result)
    print()  # Salto de línea tras el \r
    return results


def print_report(label: str, results: list) -> None:
    """
    Imprime un resumen legible de los resultados del benchmark.

    Args:
        label:   Descripción del escenario (ej. "Minimax vs Random").
        results: Lista de dicts retornada por run_benchmark().
    """
    total     = len(results)
    red_wins  = sum(1 for r in results if r["winner"] == "RED")
    blue_wins = sum(1 for r in results if r["winner"] == "BLUE")
    draws     = sum(1 for r in results if r["winner"] == "DRAW")

    avg_turns  = sum(r["turns"]          for r in results) / total
    avg_nodes  = sum(r["nodes_expanded"] for r in results) / total
    avg_depth  = sum(r["depth_reached"]  for r in results) / total
    avg_time   = sum(r["time_used"]      for r in results) / total

    print(f"\n{'=' * 52}")
    print(f"  {label}")
    print(f"{'=' * 52}")
    print(f"  Partidas jugadas : {total}")
    print(f"  RED  gana        : {red_wins}  ({red_wins/total*100:.0f}%)")
    print(f"  BLUE gana        : {blue_wins}  ({blue_wins/total*100:.0f}%)")
    print(f"  Empates          : {draws}  ({draws/total*100:.0f}%)")
    print(f"  Avg turnos       : {avg_turns:.1f}")
    print(f"  Avg nodos        : {avg_nodes:.0f}")
    print(f"  Avg profundidad  : {avg_depth:.1f}")
    print(f"  Avg tiempo       : {avg_time:.3f}s")
    print(f"{'=' * 52}")


# ── Escenarios completos del profesor ─────────────────────────────────────────

def run_all_benchmarks(num_games: int = 10) -> None:
    """
    Ejecuta TODOS los escenarios que pide el profesor y muestra los resultados.

    Ejecutar con:
        python main.py --benchmark

    Args:
        num_games: Partidas por escenario. Default 10.
                   Subir a 20-30 para resultados más confiables.
    """
    print("\n" + "=" * 52)
    print("  BENCHMARK COMPLETO — ONITAMA IA")
    print(f"  {num_games} partidas por escenario")
    print("=" * 52)

    # ── A. Minimax vs Random ──────────────────────────────────────────────────
    print("\n[1/7] Minimax vs Random...")
    results = run_benchmark(MinimaxAgent(), RandomAgent(), num_games)
    print_report("Minimax vs Random", results)

    # ── B. Minimax vs Greedy ──────────────────────────────────────────────────
    print("\n[2/7] Minimax vs Greedy...")
    results = run_benchmark(MinimaxAgent(), GreedyAgent(), num_games)
    print_report("Minimax vs Greedy", results)

    # ── C. Minimax vs Worst ───────────────────────────────────────────────────
    print("\n[3/7] Minimax vs Worst...")
    results = run_benchmark(MinimaxAgent(), WorstAgent(), num_games)
    print_report("Minimax vs WorstDecision", results)

    # ── D. Minimax (pesos 1) vs Minimax (pesos 2) ─────────────────────────────
    print("\n[4/7] Minimax config1 vs Minimax config2...")
    results = run_benchmark(
        MinimaxAgent(weights=DEFAULT_WEIGHTS),
        MinimaxAgent(weights=ALT_WEIGHTS),
        num_games
    )
    print_report("Minimax (Pesos DEFAULT) vs Minimax (Pesos ALT)", results)

    # ── E. Minimax vs Minimax (misma config) ─────────────────────────────────
    print("\n[5/7] Minimax vs Minimax (igual config)...")
    results = run_benchmark(MinimaxAgent(), MinimaxAgent(), num_games)
    print_report("Minimax vs Minimax (misma config)", results)

    # ── F. Distintas cantidades de heurísticas ────────────────────────────────
    print("\n[6/7] Variando cantidad de heurísticas...")
    for n in range(1, 6):
        print(f"  Minimax ({n} heurística(s)) vs Random...")
        results = run_benchmark(
            MinimaxAgent(heuristics_count=n),
            RandomAgent(),
            num_games
        )
        print_report(f"Minimax ({n} heuristica(s)) vs Random", results)

    # ── G. Distintos tiempos máximos ──────────────────────────────────────────
    print("\n[7/7] Variando max_time...")
    for t in [1.0, 3.0, 10.0]:
        print(f"  Minimax (max_time={t}s) vs Random...")
        results = run_benchmark(
            MinimaxAgent(max_time=t),
            RandomAgent(),
            num_games
        )
        print_report(f"Minimax (max_time={t}s) vs Random", results)

    print("\n  Benchmark finalizado.")