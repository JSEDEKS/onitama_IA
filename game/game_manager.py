from game.board import Board
from game.player import Player
from game.cards import CardManager
from game.rules import Rules
from utils.console_ui import ConsoleUI

# ── Importaciones de IA ───────────────────────────────────────────────────────
# PERSONA 4: Estos imports ya están listos. No necesitas cambiarlos.
from ai.game_state import GameState
from ai.ai_player import RandomAgent, GreedyAgent, WorstAgent, MinimaxAgent


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
                self.configure_players()   # PERSONA 4: configurar antes de iniciar
                self.start_game()
                break
            elif option == "2":
                self.ui.show_instructions()
            elif option == "3":
                exit()
            else:
                input("Opcion invalida. Presiona ENTER...")

    # ── Configuración de jugadores ────────────────────────────────────────────
    # PERSONA 4: implementar este método

    def configure_players(self):
        """
        Pregunta al usuario el tipo de cada jugador y asigna el agente correspondiente.

        PERSONA 4: Tu trabajo empieza aquí.

        Modos disponibles:
            1. Humano vs Humano   → ambos players con is_ai=False
            2. Humano vs IA       → players[1] con is_ai=True, agent=MinimaxAgent()
            3. IA vs IA           → ambos con is_ai=True y sus agentes

        Ejemplo de asignación:
            self.players[1].is_ai = True
            self.players[1].agent = MinimaxAgent(max_time=3.0)

        Agentes disponibles (importados arriba):
            RandomAgent()
            GreedyAgent()
            WorstAgent()
            MinimaxAgent(max_time=3.0, heuristics_count=5)
        """
        # TODO — Persona 4
        #
        # self.ui.clear()
        # print("Selecciona el modo de juego:")
        # print("  1. Humano vs Humano")
        # print("  2. Humano vs IA")
        # print("  3. IA vs IA")
        # mode = input("Opcion: ").strip()
        #
        # if mode == "2":
        #     self.players[1].is_ai = True
        #     self.players[1].agent = MinimaxAgent(max_time=3.0)
        # elif mode == "3":
        #     self.players[0].is_ai = True
        #     self.players[0].agent = MinimaxAgent(max_time=3.0)
        #     self.players[1].is_ai = True
        #     self.players[1].agent = MinimaxAgent(max_time=3.0)
        # # else: ambos humanos, no se hace nada
        #
        pass  # Eliminar este pass cuando implementes el método

    # ── Inicio de partida ─────────────────────────────────────────────────────

    def start_game(self):
        self.setup_game()
        self.game_loop()

    def setup_game(self):
        self.board.setup(self.players)
        self.card_manager.deal_cards(self.players)

    def get_opponent(self, player):
        return self.players[1] if player == self.players[0] else self.players[0]

    # ── Game loop principal ───────────────────────────────────────────────────

    def game_loop(self):
        while True:
            current_player = self.players[self.current_player_index]
            opponent = self.get_opponent(current_player)

            try:
                self.ui.clear()
                self.ui.show_board(self.board)
                self.ui.show_player_turn(current_player)
                self.ui.show_all_cards(current_player, opponent, self.card_manager.side_card)

                # ── Turno de la IA ────────────────────────────────────────────
                # PERSONA 4: Esta es la integración principal.
                if current_player.is_ai:
                    card, piece, destination = self._get_ai_move(current_player)

                # ── Turno del humano ──────────────────────────────────────────
                else:
                    card = self.ui.choose_card(current_player)
                    self.ui.show_card_moves(card, current_player.color)

                    pieces_with_moves = self.card_manager.get_all_valid_moves(
                        card, current_player, self.board
                    )

                    if not pieces_with_moves:
                        self.ui.show_no_moves(card)
                        self.card_manager.swap_card(current_player, card)
                        self.next_turn()
                        continue

                    all_valid = set()
                    for moves in pieces_with_moves.values():
                        all_valid.update(moves)

                    self.ui.clear()
                    self.ui.show_board(self.board, valid_moves=all_valid)
                    self.ui.show_player_turn(current_player)
                    self.ui.show_all_cards(current_player, opponent, self.card_manager.side_card)
                    print(f"\nCarta seleccionada: {card.name}")

                    piece = self.ui.choose_piece(pieces_with_moves)

                    piece_moves = pieces_with_moves[piece]
                    self.ui.clear()
                    self.ui.show_board(self.board, valid_moves=set(piece_moves))
                    self.ui.show_player_turn(current_player)
                    print(f"\nCarta: {card.name} | Pieza: {piece.type} en ({piece.position[0]},{piece.position[1]})")

                    destination = self.ui.choose_destination(piece_moves)

                # ── Ejecutar movimiento (común para humano e IA) ──────────────
                self.board.move_piece(piece.position, destination)
                self.card_manager.swap_card(current_player, card)

                if self.rules.check_victory(self.board, current_player):
                    self.ui.clear()
                    self.ui.show_board(self.board)
                    self.ui.show_winner(current_player)
                    break

                self.next_turn()

            except Exception as e:
                print(f"Ocurrio un error: {e}")
                input("Presiona ENTER para continuar...")

    # ── Movimiento de IA ──────────────────────────────────────────────────────
    # PERSONA 4: implementar este método

    def _get_ai_move(self, current_player):
        """
        Construye el GameState actual y llama al agente para que elija un movimiento.

        PERSONA 4: Tu trabajo principal está aquí.

        Retorna una tupla (card, piece, destination) con objetos REALES
        (del tablero real, no del estado copiado) para que game_loop pueda ejecutarlos.

        Pasos:
            1. Crear GameState desde el estado actual del juego.
            2. Llamar al agente: next_state = current_player.agent.choose_move(state)
            3. Extraer last_move del next_state: (card, piece, destination)
            4. Traducir card y piece del estado copiado a objetos reales del juego.
            5. Mostrar al usuario qué movimiento hizo la IA.
            6. Retornar (real_card, real_piece, destination).
        """
        # TODO — Persona 4
        #
        # state = GameState.from_game(
        #     self.board, self.players,
        #     self.card_manager, self.current_player_index
        # )
        #
        # print(f"\n  {current_player.name} (IA) está pensando...")
        # next_state = current_player.agent.choose_move(state)
        #
        # if next_state is None or next_state.last_move is None:
        #     raise Exception("La IA no pudo encontrar un movimiento.")
        #
        # ai_card, ai_piece, destination = next_state.last_move
        #
        # # Traducir a objetos reales (last_move tiene refs al estado copiado)
        # real_card  = next(c for c in current_player.cards  if c.name == ai_card.name)
        # real_piece = next(p for p in current_player.pieces if p.position == ai_piece.position)
        #
        # print(f"  IA jugó: {real_card.name} → {real_piece.type} a {destination}")
        # input("  Presiona ENTER para continuar...")
        #
        # return (real_card, real_piece, destination)
        #
        raise NotImplementedError("Persona 4: implementar _get_ai_move()")

    def next_turn(self):
        self.current_player_index = (self.current_player_index + 1) % 2
