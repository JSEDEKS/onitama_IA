"""
PERSONA 1 — ai/game_state.py
============================================================
Responsabilidad: Representar el estado del juego para el Minimax.

Esta clase es la BASE de todo el módulo AI. Todos los demás archivos
dependen de que los 3 métodos principales funcionen correctamente:
    - is_terminal()
    - eval()
    - children()

Archivos de game/ que debes leer y entender:
    - game/board.py       → self.board (grid, move_piece, get_enemy_temple)
    - game/player.py      → self.players (pieces, cards, get_master)
    - game/pieces.py      → Piece, Master, Student y sus atributos
    - game/cards.py       → self.card_manager (get_all_valid_moves, swap_card)
    - game/rules.py       → self._rules (check_victory)
============================================================
"""

import copy
from typing import Optional, Tuple, List

from game.board import Board
from game.player import Player
from game.cards import CardManager
from game.rules import Rules


class GameState:
    """
    Foto inmutable del juego en un momento dado.

    El Minimax nunca toca el juego real — trabaja solo con GameState.
    Cada vez que se aplica un movimiento, se crea un NUEVO GameState.
    """

    def __init__(
        self,
        board: Board,
        players: list,
        card_manager: CardManager,
        current_player_index: int,
        last_move=None
    ):
        """
        Constructor interno. Para crear un estado desde el juego real,
        usar el método estático GameState.from_game().

        Args:
            board:                 Tablero actual (ya copiado).
            players:               Lista [jugador_0 (RED), jugador_1 (BLUE)] (ya copiados).
            card_manager:          Gestor de cartas con side_card (ya copiado).
            current_player_index:  0 o 1 — quién le toca mover ahora.
            last_move:             Tupla (card, piece, destination) que generó este estado.
                                   None si es el estado raíz.
        """
        self.board = board
        self.players = players
        self.card_manager = card_manager
        self.current_player_index = current_player_index
        self.last_move = last_move  # (card, piece, (x, y)) — lo usa game_manager para ejecutar el movimiento real

        self._rules = Rules()

    # ──────────────────────────────────────────────────────────────────────────
    # Propiedades de conveniencia — NO modificar
    # ──────────────────────────────────────────────────────────────────────────

    @property
    def current_player(self) -> Player:
        """Jugador que debe mover en este estado."""
        return self.players[self.current_player_index]

    @property
    def opponent(self) -> Player:
        """Jugador que NO mueve en este estado."""
        return self.players[1 - self.current_player_index]

    # ──────────────────────────────────────────────────────────────────────────
    # Método de fábrica — NO modificar
    # ──────────────────────────────────────────────────────────────────────────

    @staticmethod
    def from_game(
        board: Board,
        players: list,
        card_manager: CardManager,
        current_player_index: int
    ) -> "GameState":
        """
        Crea un GameState desde los objetos reales del juego usando deepcopy.
        Este es el punto de entrada desde game_manager.py cuando la IA va a pensar.

        Ejemplo de uso en game_manager.py:
            state = GameState.from_game(
                self.board, self.players,
                self.card_manager, self.current_player_index
            )
            next_state = current_player.agent.choose_move(state)
        """
        return GameState(
            board=copy.deepcopy(board),
            players=copy.deepcopy(players),
            card_manager=copy.deepcopy(card_manager),
            current_player_index=current_player_index,
            last_move=None
        )

    # ──────────────────────────────────────────────────────────────────────────
    # MÉTODOS PRINCIPALES — PERSONA 1 debe implementar estos 3
    # ──────────────────────────────────────────────────────────────────────────

    def is_terminal(self) -> Tuple[bool, Optional[Player]]:
        """
        Verifica si el juego terminó en este estado.

        En Onitama el juego termina cuando:
            1. El maestro de un jugador es capturado.
            2. El maestro de un jugador llega al templo enemigo.

        IMPORTANTE: check_victory(board, player) comprueba si `player` GANÓ.
        Hay que verificarlo para ambos jugadores.

        Returns:
            (True,  ganador)  si el juego terminó.
            (False, None)     si el juego continúa.

        Ejemplo:
            terminal, winner = state.is_terminal()
            if terminal:
                print(f"Ganó {winner.name}")
        """
        # TODO — Persona 1
        #
        # Verificar para ambos jugadores:
        #   for player in self.players:
        #       if self._rules.check_victory(self.board, player):
        #           return (True, player)
        #   return (False, None)
        #
        raise NotImplementedError("Persona 1: implementar is_terminal()")

    def eval(self) -> float:
        """
        Valor heurístico del estado desde la perspectiva de current_player.

        Este método delega en ai/heuristics.py (trabajo de Persona 3).
        Persona 1 solo necesita hacer la llamada correcta.

        Convención de signo (MUY IMPORTANTE para que Minimax funcione):
            Valor POSITIVO  → favorable para current_player
            Valor NEGATIVO  → favorable para opponent

        Returns:
            float: puntuación heurística del estado.
        """
        # TODO — Persona 1 + Persona 3
        #
        # from ai.heuristics import evaluate
        # return evaluate(self, self.current_player)
        #
        raise NotImplementedError("Persona 1+3: implementar eval()")

    def children(self) -> List["GameState"]:
        """
        Genera todos los estados hijo posibles desde este estado.

        Por cada combinación (carta, pieza, destino) válida para current_player,
        se crea un nuevo GameState con el movimiento ya aplicado.

        Caso especial — sin movimientos disponibles:
            En Onitama, si un jugador no puede mover con ninguna carta,
            debe hacer swap de una carta y pasar el turno. En ese caso
            retornar una lista con ese único estado resultante.

        Returns:
            list[GameState]: Todos los estados alcanzables en un movimiento.
                             Cada estado tiene last_move = (card, piece, destination).
        """
        # TODO — Persona 1
        #
        # hijos = []
        #
        # for card in self.current_player.cards:
        #     pieces_with_moves = self.card_manager.get_all_valid_moves(
        #         card, self.current_player, self.board
        #     )
        #     for piece, destinations in pieces_with_moves.items():
        #         for dest in destinations:
        #             nuevo_estado = self._apply_move(card, piece, dest)
        #             hijos.append(nuevo_estado)
        #
        # if not hijos:
        #     # Sin movimientos: hacer swap de la primera carta y pasar turno
        #     card = self.current_player.cards[0]
        #     estado_swap = copy.deepcopy(self)
        #     estado_swap.card_manager.swap_card(estado_swap.current_player, card)
        #     estado_swap.current_player_index = 1 - self.current_player_index
        #     estado_swap.last_move = None
        #     hijos.append(estado_swap)
        #
        # return hijos
        #
        raise NotImplementedError("Persona 1: implementar children()")

    # ──────────────────────────────────────────────────────────────────────────
    # Método auxiliar — PERSONA 1 debe implementar
    # ──────────────────────────────────────────────────────────────────────────

    def _apply_move(self, card, piece, destination: tuple) -> "GameState":
        """
        Crea un NUEVO GameState aplicando el movimiento dado.
        NO modifica el estado actual (self permanece intacto).

        Pasos:
            1. Hacer deepcopy de self para no contaminar el estado actual.
            2. En el nuevo estado, mover la pieza en el tablero.
            3. En el nuevo estado, hacer swap de la carta usada.
            4. Cambiar el turno al otro jugador.
            5. Registrar el movimiento en last_move.

        Args:
            card:        Carta usada (objeto Card del estado copiado).
            piece:       Pieza a mover (objeto Piece del estado copiado).
            destination: Tupla (x, y) del destino.

        Returns:
            GameState: Nuevo estado resultante, listo para ser explorado.
        """
        # TODO — Persona 1
        #
        # new_state = copy.deepcopy(self)
        #
        # # Encontrar la carta y pieza equivalentes en el nuevo estado
        # # (deepcopy crea objetos nuevos, no son los mismos objetos)
        # new_card  = next(c for c in new_state.current_player.cards if c.name == card.name)
        # new_piece = next(p for p in new_state.current_player.pieces if p.position == piece.position)
        #
        # # Aplicar movimiento en el tablero copiado
        # new_state.board.move_piece(new_piece.position, destination)
        #
        # # Hacer swap de la carta
        # new_state.card_manager.swap_card(new_state.current_player, new_card)
        #
        # # Cambiar turno
        # new_state.current_player_index = 1 - self.current_player_index
        #
        # # Guardar el movimiento que generó este estado
        # new_state.last_move = (card, piece, destination)
        #
        # return new_state
        #
        raise NotImplementedError("Persona 1: implementar _apply_move()")
