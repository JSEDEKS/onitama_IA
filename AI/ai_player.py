import random
import time
from MinimaxSolver import MinimaxSolver

class RandomPlayer:
    def __init__(self):
        self.name = "Random"

    def choose_move(self, game_manager):
        moves = game_manager.get_legal_moves()
        if not moves:
            return None
        return random.choice(moves)

class GreedyPlayer:
    def __init__(self):
        self.name = "Greedy"

    def choose_move(self, game_manager):
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
        self.ai = MinimaxSolver(depth=depth)

    def choose_move(self, game_manager):
        return self.ai.get_best_move(game_manager)
