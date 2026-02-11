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
                input("Opcion invalida. Presiona ENTER...")

    def start_game(self):
        self.setup_game()
        self.game_loop()

    def setup_game(self):
        self.board.setup(self.players)
        self.card_manager.deal_cards(self.players)

    def get_opponent(self, player):
        return self.players[1] if player == self.players[0] else self.players[0]

    def game_loop(self):
        while True:
            current_player = self.players[self.current_player_index]
            opponent = self.get_opponent(current_player)

            try:
                # Mostrar estado del juego
                self.ui.clear()
                self.ui.show_board(self.board)
                self.ui.show_player_turn(current_player)
                self.ui.show_all_cards(current_player, opponent, self.card_manager.side_card)

                # Elegir carta
                card = self.ui.choose_card(current_player)

                # Mostrar patron de la carta
                self.ui.show_card_moves(card, current_player.color)

                # Calcular todos los movimientos validos con esa carta
                pieces_with_moves = self.card_manager.get_all_valid_moves(
                    card, current_player, self.board
                )

                if not pieces_with_moves:
                    # No hay movimientos validos: swap carta y pasar turno
                    self.ui.show_no_moves(card)
                    self.card_manager.swap_card(current_player, card)
                    self.next_turn()
                    continue

                # Recopilar todos los destinos validos para mostrar en el tablero
                all_valid = set()
                for moves in pieces_with_moves.values():
                    all_valid.update(moves)

                # Re-renderizar tablero con movimientos validos
                self.ui.clear()
                self.ui.show_board(self.board, valid_moves=all_valid)
                self.ui.show_player_turn(current_player)
                self.ui.show_all_cards(current_player, opponent, self.card_manager.side_card)
                print(f"\nCarta seleccionada: {card.name}")

                # Elegir pieza (solo las que pueden moverse)
                piece = self.ui.choose_piece(pieces_with_moves)

                # Re-renderizar con solo los movimientos de esa pieza
                piece_moves = pieces_with_moves[piece]
                self.ui.clear()
                self.ui.show_board(self.board, valid_moves=set(piece_moves))
                self.ui.show_player_turn(current_player)
                print(f"\nCarta: {card.name} | Pieza: {piece.type} en ({piece.position[0]},{piece.position[1]})")

                # Elegir destino
                target = self.ui.choose_destination(piece_moves)

                # Ejecutar movimiento
                self.board.move_piece(piece.position, target)
                self.card_manager.swap_card(current_player, card)

                # Verificar victoria
                if self.rules.check_victory(self.board, current_player):
                    self.ui.clear()
                    self.ui.show_board(self.board)
                    self.ui.show_winner(current_player)
                    break

                self.next_turn()

            except Exception as e:
                print(f"Ocurrio un error: {e}")
                input("Presiona ENTER para continuar...")

    def next_turn(self):
        self.current_player_index = (self.current_player_index + 1) % 2
