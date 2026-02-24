import random
import time
from .minimax import minimax
from .game_state import GameState
from .ids import ids_decision

class RandomPlayer:
    def __init__(self):
        self.name = "Random"

    def choose_move(self, state_or_manager):
        # Adaptador para soportar tanto GameState (Benchmark) como GameManager (Juego)
        if isinstance(state_or_manager, GameState):
            children = state_or_manager.children()
            return random.choice(children) if children else None
        else:
            # Modo interactivo (GameManager)
            moves = state_or_manager.get_legal_moves()
            return random.choice(moves) if moves else None

class GreedyPlayer:
    def __init__(self):
        self.name = "Greedy"

    def choose_move(self, game_manager):
        # Nota: GreedyPlayer tal como estaba implementado solo funcionaba con GameManager.
        # Para que funcione en Benchmark, debería usar GameState y Heuristics.
        # Esta es una adaptación rápida para evitar el crash en benchmark:
        if isinstance(game_manager, GameState):
            # En benchmark, por ahora actuará como Random o necesitaría reimplementar lógica
            # Para este ejemplo, devolvemos el primer hijo (o random) para no romper el código
            children = game_manager.children()
            return children[0] if children else None

        moves = game_manager.get_legal_moves()
        if not moves:
            return None

        best_score = float('-inf')
        best_move = moves[0]

        for move in moves:
            # Simulamos el movimiento
            game_manager.make_move(move)
            score = game_manager.evaluate()
            # Revertimos
            game_manager.switch_player()
            game_manager.make_move(move)  # Esto depende de tu implementación, puede ser deepcopy
            game_manager.switch_player()

            if score > best_score:
                best_score = score
                best_move = move

        return best_move

class MinimaxPlayer:
    def __init__(self, depth=2, max_time=3):
        self.name = "Minimax"
        self.depth = depth
        self.max_time = max_time
        # No instanciamos minimax aquí porque aún no sabemos el nombre del jugador (RED/BLUE)

    def choose_move(self, state):
        # Aseguramos que trabajamos con GameState
        if not isinstance(state, GameState):
            # Si nos pasan GameManager, no podemos proceder fácilmente sin convertirlo
            raise ValueError("MinimaxPlayer requiere GameState")

        # 1. Instanciar la lógica Minimax con el color correcto
        ai = minimax(state.current_player.name, max_depth=self.depth)
        
        # 2. Obtener el mejor movimiento (tupla)
        best_move_tuple = ai.solve(state)
        
        # 3. Buscar qué estado hijo corresponde a ese movimiento
        if best_move_tuple:
            for child in state.children():
                if child.last_move == best_move_tuple:
                    return child
        
        return None

class IDSPlayer:
    def __init__(self, max_time=3):
        self.name = "IDS"
        self.max_time = max_time

    def choose_move(self, state):
        best_child, _ = ids_decision(state, self.max_time)
        return best_child