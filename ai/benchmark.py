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
from typing import Any

from game.board import Board
from game.player import Player
from game.cards import CardManager
from game.rules import Rules
from ai.game_state import GameState
from ai.ai_player import RandomPlayer, GreedyPlayer, MinimaxPlayer, WorstPlayer, IDSPlayer
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

def run_match(agent1: Any, agent2: Any) -> dict:
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
            "final_score":    float,  # Puntos obtenidos (heurística final)
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
    heuristics_calc = Heuristics()

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
        if state.is_terminal():
            points = state.get_winner_points()
            winner_color = "DRAW"
            for name, score in points.items():
                if score == 1:
                    winner_color = name
                    break

            # Calcular puntaje final del ganador (o del rojo si empate)
            winner_obj = players[0] if winner_color == "RED" else players[1]
            final_score = heuristics_calc.evaluate(state, winner_obj)

            return {
                "winner":         winner_color,
                "turns":          turn,
                "nodes_expanded": total_nodes,
                "depth_reached":  max_depth,
                "time_used":      round(time.time() - start_time, 4),
                "final_score":    round(final_score, 2)
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
    # Evaluamos desde la perspectiva de RED
    final_score = heuristics_calc.evaluate(state, players[0])
    
    return {
        "winner":         "DRAW",
        "turns":          MAX_TURNS,
        "nodes_expanded": total_nodes,
        "depth_reached":  max_depth,
        "time_used":      round(time.time() - start_time, 4),
        "final_score":    round(final_score, 2)
    }


# ── Suite de benchmarks ───────────────────────────────────────────────────────

def run_benchmark(agent1: object, agent2: object, num_games: int = 10) -> list:
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
    avg_score  = sum(r["final_score"]    for r in results) / total

    print(f"\n{'=' * 52}")
    print(f"  {label}")
    print(f"{'=' * 52}")
    print(f"  Partidas jugadas : {total}")
    print(f"  RED  gana        : {red_wins}  ({red_wins/total*100:.0f}%)")
    print(f"  BLUE gana        : {blue_wins}  ({blue_wins/total*100:.0f}%)")
    print(f"  Empates          : {draws}  ({draws/total*100:.0f}%)")
    print(f"  --------------------------------")
    print(f"  Avg turnos       : {avg_turns:.1f}")
    print(f"  Avg nodos        : {avg_nodes:.0f}")
    print(f"  Avg profundidad  : {avg_depth:.1f}")
    print(f"  Avg puntos final : {avg_score:.2f}")
    print(f"  Avg tiempo       : {avg_time:.3f}s")
    print(f"{'=' * 52}\n")


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

    # Perfiles de pesos definidos en Heuristics
    profiles = Heuristics.PROFILES

    # ── A. Minimax vs Random ──────────────────────────────────────────────────
    print("\n[A] Minimax vs Random (Aleatorio)...")
    results = run_benchmark(MinimaxPlayer(), RandomPlayer(), num_games)
    print_report("Minimax vs Random", results)

    # ── B. Minimax vs Greedy ──────────────────────────────────────────────────
    print("\n[B] Minimax vs Greedy (Avaro)...")
    results = run_benchmark(MinimaxPlayer(), GreedyPlayer(), num_games)
    print_report("Minimax vs Greedy", results)

    # ── C. Minimax vs Worst ───────────────────────────────────────────────────
    print("\n[C] Minimax vs Worst (Peores decisiones)...")
    results = run_benchmark(MinimaxPlayer(), WorstPlayer(), num_games)
    print_report("Minimax vs Worst", results)

    # ── D. Humano Experto ─────────────────────────────────────────────────────
    print("\n[D] Minimax vs Humano Experto")
    print("    >> Esta prueba debe realizarse manualmente desde el Menú Principal (Opción 2).")

    # ── E. Minimax vs Minimax (misma config) ─────────────────────────────────
    print("\n[E] Minimax vs Minimax (Misma IA)...")
    results = run_benchmark(MinimaxPlayer(), MinimaxPlayer(), num_games)
    print_report("Minimax vs Minimax", results)

    # ── COMPARACIÓN DE VARIABLES ──────────────────────────────────────────────
    print("\n" + "=" * 52)
    print("  COMPARACIÓN DE VARIABLES")
    print("=" * 52)

    # i & ii. Comparación de Pesos (Config 1 vs Config 2)
    print("\n[Var i-ii] Minimax (Config 1: AGGRESSIVE) vs Minimax (Config 2: DEFENSIVE)...")
    results = run_benchmark(
        MinimaxPlayer(weights=profiles["AGGRESSIVE"]),
        MinimaxPlayer(weights=profiles["DEFENSIVE"]),
        num_games
    )
    print_report("Config 1 (RED) vs Config 2 (BLUE)", results)

    # iii - vii. Cantidad de Heurísticas (1 a 5)
    print("\n[Var iii-vii] Minimax con 1, 2, 3, 4, 5 Heurísticas (vs Random)...")
    for h in range(1, 6):
        print(f"  -> Probando con {h} heurística(s)...")
        results = run_benchmark(
            MinimaxPlayer(heuristics_count=h),
            RandomPlayer(),
            num_games
        )
        print_report(f"Minimax ({h} Heurísticas) vs Random", results)

    # viii - x. Minimax con Tiempo Máximo (1s, 3s, 10s)
    # Usamos IDSPlayer ya que es el que maneja restricciones de tiempo
    print("\n[Var viii-x] Minimax con Tiempo Máximo (1s, 3s, 10s)...")
    for t in [1.0, 3.0, 10.0]:
        print(f"  -> Probando con max_time = {t}s...")
        results = run_benchmark(
            IDSPlayer(max_time=t),
            RandomPlayer(),
            num_games
        )
        print_report(f"Minimax (Time={t}s) vs Random", results)

    print("\n  Benchmark finalizado.")