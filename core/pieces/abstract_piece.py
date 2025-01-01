from abc import ABC
from os import getcwd
from ..tools import Position, Path
from ..tools.pieces import PieceColor, PieceDirection, PieceId, PieceIsKilled, PieceIsMoved


class AbstractPiece(ABC):
    def __init__(self, pos_x: int, pos_y: int, color: str, direction: str) -> None:
        self.position: Position = Position(pos_x, pos_y)
        self.color: PieceColor = PieceColor(color)
        self.direction: PieceDirection = PieceDirection(direction)
        self.picture_path: Path = Path(f"{getcwd()}\\media\\images\\pieces\\{str(self.color)}")
        self.is_killed: PieceIsKilled = PieceIsKilled(False)
        self.is_move = PieceIsMoved(False)
        self.id: PieceId = PieceId()

