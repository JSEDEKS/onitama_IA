import copy
from game.rules import Rules

class GameState:
    """
    Representa una 'foto' del estado del juego en un momento dado.
    Es fundamental para que el algoritmo Minimax pueda simular movimientos
    sin alterar el juego real.
    """

    def __init__(self, board, players, card_manager, current_player_index, turn_count=0):
        self.board = board
        self.players = players
        self.card_manager = card_manager
        self.current_player_index = current_player_index
        self.turn_count = turn_count
        self.rules = Rules()

    def get_current_player(self):
        return self.players[self.current_player_index]

    def get_opponent(self, player):
        # Retorna el otro jugador (asumiendo 2 jugadores)
        return self.players[1] if player == self.players[0] else self.players[0]

    def get_all_moves(self, player):
        """
        Retorna todos los movimientos posibles para el jugador dado.
        Formato: lista de tuplas (card, piece, destination)
        """
        moves = []
        # Iteramos sobre las 2 cartas del jugador
        for card in player.cards:
            # card_manager.get_all_valid_moves retorna {piece: [destinations]}
            pieces_moves = self.card_manager.get_all_valid_moves(card, player, self.board)
            
            for piece, destinations in pieces_moves.items():
                for dest in destinations:
                    moves.append((card, piece, dest))
        return moves

    def apply_move(self, card, piece, dest):
        """
        Genera un NUEVO estado resultante de aplicar el movimiento.
        NO modifica el estado actual (inmutabilidad para Minimax).
        """
        # 1. Clonar todo el estado (Deep Copy para romper referencias con el juego real)
        # Al copiar 'self', copiamos recursivamente board, players y card_manager manteniendo sus relaciones
        new_state = copy.deepcopy(self)
        
        # 2. Obtener las referencias equivalentes en el nuevo mundo clonado
        current_player = new_state.get_current_player()
        
        # Buscar la carta equivalente por nombre (la instancia es distinta tras el copy)
        card_to_use = next(c for c in current_player.cards if c.name == card.name)
        
        # 3. Ejecutar el movimiento en el tablero clonado
        # Nota: move_piece usa coordenadas (piece.position), así que funciona aunque 'piece' sea del estado anterior
        new_state.board.move_piece(piece.position, dest)
        
        # 4. Rotar cartas en el manager clonado
        new_state.card_manager.swap_card(current_player, card_to_use)
        
        # 5. Avanzar turno
        new_state.current_player_index = (new_state.current_player_index + 1) % 2
        new_state.turn_count += 1
        
        return new_state

    def is_terminal(self):
        """
        Verifica si el juego ha terminado en este estado.
        Retorna: (bool is_game_over, Player winner)
        """
        # Verificamos victoria para ambos jugadores
        # (Normalmente basta chequear al que acaba de mover, pero esto es más seguro)
        for player in self.players:
            if self.rules.check_victory(self.board, player):
                return True, player
        
        return False, None