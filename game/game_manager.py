import time
from game.board import Board
from game.player import Player
from game.cards import CardManager
from game.rules import Rules
from utils.console_ui import ConsoleUI
from ai.game_state import GameState
from ai.ai_player import RandomPlayer, MinimaxPlayer, IDSPlayer


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
        self.ai_opponent = None  # Si es None, es Humano vs Humano

    def start(self):
        self.show_menu()

    def show_menu(self):
        while True:
            self.ui.clear()
            self.ui.show_main_menu()
            option = self.ui.choose_menu_option()

            if option == "1":
                self.ai_opponent = None
                self.start_game()
                break
            elif option == "2":
                self.setup_ai()
                self.start_game()
                break
            elif option == "3":
                self.ui.show_instructions()
            elif option == "4":
                exit()
            else:
                input("Opcion invalida. Presiona ENTER...")

    def setup_ai(self):
        print("\n" + self.ui.BOLD + "Selecciona dificultad:" + self.ui.RESET)
        print("1. Facil (Random)")
        print("2. Medio (Minimax - Profundidad 3)")
        print("3. Dificil (IDS - 2 segundos)")
        
        while True:
            choice = input("Opcion: ")
            if choice == "1":
                self.ai_opponent = RandomPlayer()
                break
            elif choice == "2":
                self.ai_opponent = MinimaxPlayer(depth=3)
                break
            elif choice == "3":
                self.ai_opponent = IDSPlayer(max_time=2.0)
                break
            print("Opcion invalida.")
        
        # Configurar nombre de la IA
        self.players[1].name = f"IA ({self.ai_opponent.name})"

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

            # ─── TURNO DE LA IA ──────────────────────────────────────────────
            if self.ai_opponent and current_player.color == "BLUE":
                self.ui.clear()
                self.ui.show_board(self.board)
                self.ui.show_player_turn(current_player)
                print(f"Pensando...")

                # 1. Crear estado actual para la IA
                state = GameState.from_game(self.board, self.players, self.card_manager, self.current_player_index)
                
                # 2. Obtener decisión de la IA
                next_state = self.ai_opponent.choose_move(state)

                if next_state and next_state.last_move:
                    card_name, start_pos, end_pos = next_state.last_move
                    
                    # 3. Traducir y aplicar movimiento en el juego real
                    real_card = next(c for c in current_player.cards if c.name == card_name)
                    real_piece = next(p for p in current_player.pieces if p.position == start_pos)
                    
                    print(f"IA mueve {real_piece.type} a {end_pos} usando {card_name}")
                    time.sleep(1)  # Pequeña pausa para que el humano vea qué pasó
                    
                    self.board.move_piece(real_piece.position, end_pos)
                    self.card_manager.swap_card(current_player, real_card)
                else:
                    # Caso raro: no hay movimientos, pasar turno (swap forzado)
                    print("IA no tiene movimientos validos. Pasa turno.")
                    real_card = current_player.cards[0]
                    self.card_manager.swap_card(current_player, real_card)
                    time.sleep(1)

                # Verificar victoria
                if self.rules.check_victory(self.board, current_player):
                    self.ui.clear()
                    self.ui.show_board(self.board)
                    self.ui.show_winner(current_player)
                    break

                self.next_turn()
                continue
            # ─────────────────────────────────────────────────────────────────

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
