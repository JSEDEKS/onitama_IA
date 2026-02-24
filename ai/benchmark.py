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
    E. MinimaxAgent vs MinimaxAgent (mismo config)
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
    - ai/ids.py         (Persona 5 — mismo archivo)
    - game/board.py, game/player.py, game/cards.py, game/rules.py
============================================================
"""

import time
import copy

from game.board import Board
from game.player import Player
from game.cards import CardManager
from game.rules import Rules
from ai.game_state import GameState
from ai.ai_player import BaseAgent, RandomAgent, GreedyAgent, WorstAgent, MinimaxAgent
from ai.heuristics import DEFAULT_WEIGHTS, ALT_WEIGHTS


# ── Motor de partida silenciosa (sin UI) ──────────────────────────────────────

def run_match(agent1: BaseAgent, agent2: BaseAgent) -> dict:
    """
    Ejecuta una partida completa entre dos agentes sin mostrar nada en pantalla.

    agent1 juega como RED  (jugador 0, índice 0)
    agent2 juega como BLUE (jugador 1, índice 1)

    Args:
        agent1: Agente que controla a RED.
        agent2: Agente que controla a BLUE.

    Returns:
        dict con los resultados de la partida:
        {
            "winner":         str   — "RED", "BLUE" o "DRAW" (si supera max turnos),
            "turns":          int   — número de turnos jugados,
            "nodes_expanded": int   — total de nodos expandidos (si los agentes los reportan),
            "depth_reached":  int   — profundidad máxima alcanzada,
            "time_used":      float — tiempo total de la partida en segundos
        }
    """
    # TODO — Persona 5
    #
    # 1. Inicializar tablero, jugadores y cartas (como lo hace GameManager.setup_game)
    #       board = Board()
    #       players = [Player("RED", "RED"), Player("BLUE", "BLUE")]
    #       card_manager = CardManager()
    #       board.setup(players)
    #       card_manager.deal_cards(players)
    #       rules = Rules()
    #
    # 2. Asignar agentes a jugadores
    #       agents = [agent1, agent2]
    #
    # 3. Loop de juego (máximo 200 turnos para evitar partidas infinitas)
    #       start_time = time.time()
    #       current_index = 0
    #       for turn in range(200):
    #           state = GameState.from_game(board, players, card_manager, current_index)
    #
    #           terminal, winner = state.is_terminal()
    #           if terminal:
    #               return {"winner": winner.color, "turns": turn, ...}
    #
    #           next_state = agents[current_index].choose_move(state)
    #           if next_state is None or next_state.last_move is None:
    #               break
    #
    #           # Ejecutar el movimiento en el juego real
    #           card, piece, destination = next_state.last_move
    #           # Buscar la pieza real (last_move tiene referencias al estado copiado)
    #           real_piece = _find_real_piece(players[current_index], piece.position)
    #           real_card  = _find_real_card(players[current_index], card.name)
    #           board.move_piece(real_piece.position, destination)
    #           card_manager.swap_card(players[current_index], real_card)
    #           current_index = 1 - current_index
    #
    #       return {"winner": "DRAW", "turns": 200, ...}
    #
    raise NotImplementedError("Persona 5: implementar run_match()")


def _find_real_piece(player, position):
    """Busca la pieza real del jugador por posición (auxiliar de run_match)."""
    # TODO — Persona 5
    # for piece in player.pieces:
    #     if piece.position == position:
    #         return piece
    # return None
    raise NotImplementedError("Persona 5: implementar _find_real_piece()")


def _find_real_card(player, card_name):
    """Busca la carta real del jugador por nombre (auxiliar de run_match)."""
    # TODO — Persona 5
    # for card in player.cards:
    #     if card.name == card_name:
    #         return card
    # return None
    raise NotImplementedError("Persona 5: implementar _find_real_card()")


# ── Suite de benchmarks ───────────────────────────────────────────────────────

def run_benchmark(agent1: BaseAgent, agent2: BaseAgent, num_games: int = 10) -> list:
    """
    Ejecuta múltiples partidas entre dos agentes y retorna los resultados.

    Args:
        agent1:    Primer agente.
        agent2:    Segundo agente.
        num_games: Número de partidas a jugar.

    Returns:
        list[dict]: Lista de resultados, uno por partida.
    """
    # TODO — Persona 5
    #
    # results = []
    # for i in range(num_games):
    #     print(f"  Partida {i+1}/{num_games}...", end="\r")
    #     result = run_match(agent1, agent2)
    #     results.append(result)
    # print()
    # return results
    #
    raise NotImplementedError("Persona 5: implementar run_benchmark()")


def print_report(label: str, results: list) -> None:
    """
    Imprime un resumen legible de los resultados del benchmark.

    Args:
        label:   Descripción del escenario (ej. "Minimax vs Random").
        results: Lista de dicts retornada por run_benchmark().
    """
    # TODO — Persona 5
    #
    # red_wins  = sum(1 for r in results if r["winner"] == "RED")
    # blue_wins = sum(1 for r in results if r["winner"] == "BLUE")
    # draws     = sum(1 for r in results if r["winner"] == "DRAW")
    # avg_turns = sum(r["turns"] for r in results) / len(results)
    # avg_time  = sum(r["time_used"] for r in results) / len(results)
    #
    # print(f"\n{'='*50}")
    # print(f"  {label}")
    # print(f"{'='*50}")
    # print(f"  RED gana:    {red_wins}/{len(results)}")
    # print(f"  BLUE gana:   {blue_wins}/{len(results)}")
    # print(f"  Empates:     {draws}/{len(results)}")
    # print(f"  Avg turnos:  {avg_turns:.1f}")
    # print(f"  Avg tiempo:  {avg_time:.3f}s")
    # print(f"{'='*50}\n")
    #
    raise NotImplementedError("Persona 5: implementar print_report()")


# ── Escenarios completos del profesor ─────────────────────────────────────────

def run_all_benchmarks(num_games: int = 10) -> None:
    """
    Ejecuta TODOS los escenarios que pide el profesor y muestra los resultados.

    Escenarios:
        1. Minimax vs Random
        2. Minimax vs Greedy
        3. Minimax vs Worst
        4. Minimax (DEFAULT_WEIGHTS) vs Minimax (ALT_WEIGHTS)
        5. Minimax vs Minimax (misma config)
        6. Minimax con 1 heurística vs Random
           Minimax con 2 heurísticas vs Random
           ... hasta 5 heurísticas
        7. Minimax max_time=1s vs Random
           Minimax max_time=3s vs Random
           Minimax max_time=10s vs Random

    Args:
        num_games: Partidas por escenario (default 10, subir para mayor precisión).
    """
    # TODO — Persona 5
    #
    # print("\n" + "="*50)
    # print("  BENCHMARK COMPLETO — ONITAMA IA")
    # print("="*50)
    #
    # # 1. vs Random
    # results = run_benchmark(MinimaxAgent(), RandomAgent(), num_games)
    # print_report("Minimax vs Random", results)
    #
    # # 2. vs Greedy
    # results = run_benchmark(MinimaxAgent(), GreedyAgent(), num_games)
    # print_report("Minimax vs Greedy", results)
    #
    # # 3. vs Worst
    # results = run_benchmark(MinimaxAgent(), WorstAgent(), num_games)
    # print_report("Minimax vs Worst", results)
    #
    # # 4. Distintos pesos
    # results = run_benchmark(
    #     MinimaxAgent(weights=DEFAULT_WEIGHTS),
    #     MinimaxAgent(weights=ALT_WEIGHTS),
    #     num_games
    # )
    # print_report("Minimax (Pesos 1) vs Minimax (Pesos 2)", results)
    #
    # # 5. IA vs IA misma config
    # results = run_benchmark(MinimaxAgent(), MinimaxAgent(), num_games)
    # print_report("Minimax vs Minimax (misma config)", results)
    #
    # # 6. Distintas cantidades de heurísticas
    # for n in range(1, 6):
    #     results = run_benchmark(MinimaxAgent(heuristics_count=n), RandomAgent(), num_games)
    #     print_report(f"Minimax ({n} heurística(s)) vs Random", results)
    #
    # # 7. Distintos tiempos
    # for t in [1.0, 3.0, 10.0]:
    #     results = run_benchmark(MinimaxAgent(max_time=t), RandomAgent(), num_games)
    #     print_report(f"Minimax (max_time={t}s) vs Random", results)
    #
    raise NotImplementedError("Persona 5: implementar run_all_benchmarks()")