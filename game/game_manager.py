from game.board import Board
from game.player import Player
from game.cards import CardManager
from game.rules import Rules
from utils.console_ui import ConsoleUI


class GameManager:

    def __init__(self):
        self.board = Board()
        self.ui = ConsoleUI()
        self.rules = Rules()

        self.players = [
            Player("Jugador 1", "RED"),
            Player("Jugador 2", "BLUE")
        ]

        self.card_manager = CardManager()
        self.current_player_index = 0

    def start(self):
        self.show_menu()

    def show_menu(self):
        while True:
            self.ui.clear()
            self.ui.show_main_menu()
            option = self.ui.choose_menu_option()

            if option == "1":
                self.start_game()
                break
            elif option == "2":
                self.ui.show_instructions()
            elif option == "3":
                exit()
            else:
                input("Opción inválida. Presiona ENTER...")

    def start_game(self):
        self.setup_game()
        self.game_loop()

    def setup_game(self):
        self.board.setup(self.players)
        self.card_manager.deal_cards(self.players)

    def game_loop(self):
        while True:
            current_player = self.players[self.current_player_index]

            self.ui.clear()
            self.ui.show_board(self.board)
            self.ui.show_player_turn(current_player)

            card = self.ui.choose_card(current_player)
            piece, target = self.ui.choose_move(current_player)

            self.board.move_piece(piece.position, target)
            self.card_manager.swap_card(current_player, card)

            if self.rules.check_victory(self.board, current_player):
                self.ui.show_winner(current_player)
                break

            self.next_turn()

    def next_turn(self):
        self.current_player_index = (self.current_player_index + 1) % 2


    def game_loop(self):
        while True:
            current_player = self.players[self.current_player_index]

            self.ui.clear()
            self.ui.show_board(self.board)
            self.ui.show_player_turn(current_player)

            try:
                card = self.ui.choose_card(current_player)
                piece, target = self.ui.choose_move(current_player)

                self.board.move_piece(piece.position, target)
                self.card_manager.swap_card(current_player, card)

                if self.rules.check_victory(self.board, current_player):
                    self.ui.show_winner(current_player)
                    break

                self.next_turn()

            except Exception as e:
                print("❌ Ocurrió un error. Intenta de nuevo.")
                print(f"Detalle: {e}")
                input("Presiona ENTER para continuar...")

