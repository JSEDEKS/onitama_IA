import random
import time
from .minimax import minimax
from .game_state import GameState
from .ids import ids_decision
from .heuristics import Heuristics

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
        self.heuristics = Heuristics()

    def choose_move(self, game_manager):
        if isinstance(game_manager, GameState):
            # Lógica correcta para Benchmark usando tus Heurísticas
            children = game_manager.children()
            if not children:
                return None
            
            best_score = float('-inf')
            best_child = children[0]
            
            # Greedy solo mira 1 paso adelante (profundidad 0 o 1)
            for child in children:
                score = self.heuristics.evaluate(child, game_manager.current_player)
                if score > best_score:
                    best_score = score
                    best_child = child
            return best_child

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

class WorstPlayer:
    def __init__(self):
        self.name = "Worst"
        self.heuristics = Heuristics()

    def choose_move(self, game_manager):
        # Adaptación para Benchmark (GameState)
        if isinstance(game_manager, GameState):
            children = game_manager.children()
            if not children: return None
            
            worst_score = float('inf')
            worst_child = children[0]
            
            for child in children:
                # Evaluamos qué tan bueno es el estado para mí
                score = self.heuristics.evaluate(child, game_manager.current_player)
                # Buscamos el MENOR puntaje (jugar mal a propósito)
                if score < worst_score:
                    worst_score = score
                    worst_child = child
            return worst_child
        return None

class MinimaxPlayer:
    def __init__(self, depth=2, max_time=3, heuristics_count=5, weights=None):
        self.name = "Minimax"
        self.depth = depth
        self.max_time = max_time
        self.heuristics_count = heuristics_count
        self.weights = weights
        # No instanciamos minimax aquí porque aún no sabemos el nombre del jugador (RED/BLUE)

    def choose_move(self, state):
        # Aseguramos que trabajamos con GameState
        if not isinstance(state, GameState):
            # Si nos pasan GameManager, no podemos proceder fácilmente sin convertirlo
            raise ValueError("MinimaxPlayer requiere GameState")

        # 1. Instanciar la lógica Minimax con el color correcto
        ai = minimax(
            state.current_player.name, 
            max_depth=self.depth,
            heuristics_count=self.heuristics_count,
            weights=self.weights
        )
        
        # 2. Obtener el mejor movimiento (tupla)
        best_move_tuple = ai.solve(state)
        
        # 3. Buscar qué estado hijo corresponde a ese movimiento
        if best_move_tuple:
            for child in state.children():
                if child.last_move == best_move_tuple:
                    return child
        
        return None

class IDSPlayer:
    def __init__(self, max_time=3, heuristics_count=5, weights=None):
        self.name = "IDS"
        self.max_time = max_time
        self.heuristics_count = heuristics_count
        self.weights = weights

    def choose_move(self, state):
        best_child, _ = ids_decision(state, self.max_time, self.heuristics_count, self.weights)
        return best_child