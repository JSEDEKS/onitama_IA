
from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from game.player import Player

Position = Tuple[int, int]  


@dataclass(eq=False)
class Piece:
    owner: "Player"
    position: Position
    type: str  

    def move(self, new_position: Position) -> None:
        self.position = new_position


class Master(Piece):
    def __init__(self, owner: "Player", position: Position):
        super().__init__(owner=owner, position=position, type="MASTER")


class Student(Piece):
    def __init__(self, owner: "Player", position: Position):
        super().__init__(owner=owner, position=position, type="STUDENT")