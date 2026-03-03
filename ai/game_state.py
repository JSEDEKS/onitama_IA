import copy
from typing import List

from game.rules import Rules


class GameState:

    def __init__(
        self,
        board,
        players,
        card_manager,
        current_player_index,
        last_move=None
    ):
        self.board = board
        self.players = players
        self.card_manager = card_manager
        self.current_player_index = current_player_index
        self.last_move = last_move

        self._rules = Rules()

    # ─────────────────────────────────────
    # PROPIEDADES
    # ─────────────────────────────────────

    @property
    def current_player(self):
        return self.players[self.current_player_index]

    @property
    def opponent(self):
        return self.players[1 - self.current_player_index]

    # ─────────────────────────────────────
    # FACTORY
    # ─────────────────────────────────────

    @staticmethod
    def from_game(board, players, card_manager, current_player_index):
        # Empaquetamos todo para que deepcopy mantenga las referencias cruzadas
        # (Board -> Piece -> Player) y (Player -> Piece).
        # Si copiamos por separado, se rompen los enlaces y se desincronizan.
        data = {
            "board": board,
            "players": players,
            "card_manager": card_manager
        }
        copied_data = copy.deepcopy(data)

        return GameState(
            board=copied_data["board"],
            players=copied_data["players"],
            card_manager=copied_data["card_manager"],
            current_player_index=current_player_index
        )

    # ─────────────────────────────────────
    # MÉTODOS QUE USA MINIMAX
    # ─────────────────────────────────────

    def is_terminal(self) -> bool:
        
        for player in self.players:
            if self._rules.check_victory(self.board, player):
                return True
        return False

    def get_winner_points(self):
      

        for player in self.players:
            if self._rules.check_victory(self.board, player):
                winner = player
                loser = self.players[1 - self.players.index(player)]

                return {
                    winner.name: 1,
                    loser.name: -1
                }

        # No terminal
        return {player.name: 0 for player in self.players}

    def children(self) -> List["GameState"]:

        children_states = []

        for card in self.current_player.cards:
            moves_dict = self.card_manager.get_all_valid_moves(
                card,
                self.current_player,
                self.board
            )

            for piece, destinations in moves_dict.items():
                for dest in destinations:
                    new_state = self._apply_move(card, piece, dest)
                    children_states.append(new_state)

        # Si no hay movimientos → swap obligatorio
        if not children_states:
            new_state = copy.deepcopy(self)

            card = new_state.current_player.cards[0]
            new_state.card_manager.swap_card(
                new_state.current_player,
                card
            )

            new_state.current_player_index = (
                1 - new_state.current_player_index
            )

            new_state.last_move = None
            children_states.append(new_state)

        return children_states

    # ─────────────────────────────────────
    # MÉTODOS PARA HEURÍSTICAS
    # ─────────────────────────────────────

    def get_opponent(self, player):
        return self.players[1] if player == self.players[0] else self.players[0]

    def get_all_moves(self, player):
        """Retorna una lista de tuplas (card, piece, destination) con todos los movimientos posibles."""
        moves = []
        for card in player.cards:
            moves_dict = self.card_manager.get_all_valid_moves(card, player, self.board)
            for piece, destinations in moves_dict.items():
                for dest in destinations:
                    moves.append((card, piece, dest))
        return moves

    # ─────────────────────────────────────
    # AUXILIAR
    # ─────────────────────────────────────

    def _apply_move(self, card, piece, destination):

        new_state = copy.deepcopy(self)

        current_player = new_state.players[self.current_player_index]

        # buscar carta equivalente
        new_card = next(
            c for c in current_player.cards
            if c.name == card.name
        )

        # buscar pieza equivalente por posición
        new_piece = next(
            p for p in current_player.pieces
            if p.position == piece.position
        )

        # mover pieza
        new_state.board.move_piece(
            new_piece.position,
            destination
        )

        # swap carta
        new_state.card_manager.swap_card(
            current_player,
            new_card
        )

        # cambiar turno
        new_state.current_player_index = (
            1 - self.current_player_index
        )

        # guardar movimiento
        new_state.last_move = (
            card.name,
            piece.position,
            destination
        )

        return new_state