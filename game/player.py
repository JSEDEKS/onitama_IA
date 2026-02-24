from __future__ import annotations
from typing import Dict, List, Tuple, Optional

from game.pieces import Master, Student, Piece, Position

class Player:
    def __init__(self, name: str, color: str, is_ai: bool = False, ai_agent=None):
        self.name = name
        self.color = color
        self.pieces: List[Piece] = []
        self.cards = []
        self.is_ai = is_ai        # True si es jugador IA
        self.ai_agent = ai_agent  # Instancia de la clase AI correspondiente

    def create_pieces(self, positions: Dict[str, object]) -> None:
        """
        positions esperado:
        {
            "master": (x, y),
            "students": [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]
        }
        """
        master_pos = positions["master"]
        students_pos = positions["students"]

        self.pieces.append(Master(self, master_pos))
        for pos in students_pos:
            self.pieces.append(Student(self, pos))

    def get_master(self) -> Optional[Piece]:
        for piece in self.pieces:
            if piece.type == "MASTER":
                return piece
        return None

    def has_master(self) -> bool:
        return self.get_master() is not None

    def remove_piece(self, piece: Piece) -> None:
        
        if piece in self.pieces:
            self.pieces.remove(piece)
