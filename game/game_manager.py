from MinimaxSolver import MinimaxSolver
from game.board import Board
from game.player import Player
from game.rules import Rules
from AI.ai_player import RandomPlayer, GreedyPlayer, MinimaxPlayer

class GameManager:

    def __init__(self):
        self.board = Board()
        self.rules = Rules()

        print("Seleccione modo de juego:")
        print("1. Humano vs Humano")
        print("2. Humano vs IA")
        print("3. IA vs IA")
        mode = input("Opción: ")

        if mode == "1":
            self.player1 = Player("HUMAN")
            self.player2 = Player("HUMAN")
        elif mode == "2":
            self.player1 = Player("HUMAN")
            self.player2 = Player("AI", is_ai=True, ai_agent=MinimaxPlayer())
        elif mode == "3":
            self.player1 = Player("AI", is_ai=True, ai_agent=MinimaxPlayer())
            self.player2 = Player("AI", is_ai=True, ai_agent=GreedyPlayer())
        else:
            print("Opción no válida. Por defecto Humano vs IA.")
            self.player1 = Player("HUMAN")
            self.player2 = Player("AI", is_ai=True, ai_agent=MinimaxPlayer())

        self.current_player = self.player1

    def play(self):
        while not self.is_terminal():
            print("\nTurno de:", self.current_player.name)
            print(self.board)

            if self.current_player.is_ai:
                self.ai_turn()
            else:
                self.human_turn()

            self.switch_player()

        print("\nJuego terminado")
        print("Ganador:", self.get_winner())

    def human_turn(self):
        moves = self.get_legal_moves()
        if not moves:
            return

        print("Movimientos disponibles:")
        for i, move in enumerate(moves):
            print(f"{i}: {move}")

        choice = int(input("Elige movimiento: "))
        selected_move = moves[choice]
        self.make_move(selected_move)

    def ai_turn(self):
        print("La IA está pensando...")
        best_move = self.current_player.ai_agent.choose_move(self)
        if best_move is None:
            return
        print("Movimiento IA:", best_move)
        self.make_move(best_move)

    def get_legal_moves(self):
        return self.rules.get_legal_moves(self.board, self.current_player)

    def make_move(self, move):
        self.rules.apply_move(self.board, move)

    def is_terminal(self):
        return self.rules.is_game_over(self.board)

    def get_winner(self):
        return self.rules.get_winner(self.board)

    def evaluate(self):
        winner = self.get_winner()
        if winner == "AI":
            return 100
        elif winner == "HUMAN":
            return -100
        else:
            return 0

    def switch_player(self):
        if self.current_player == self.player1:
            self.current_player = self.player2
        else:
            self.current_player = self.player1
