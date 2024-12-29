from abc import ABC
from os import getcwd
from ..tools import Position, Path
from ..tools.pieces import PieceColor, PieceDirection, PieceId, PieceIsKilled


class AbstractPieces(ABC):
    def __init__(self, pos_x: int, pos_y: int, color: str) -> None:
        self.position: Position = Position(pos_x, pos_y)
        self.color: PieceColor = PieceColor()
        self.is_killed: PieceIsKilled = PieceIsKilled()
        self.direction: PieceDirection = PieceDirection()
        self.picture_path: Path = Path(f"{getcwd()}\\media\\images\\pieces\\{str(self.color)}")
        self.id: PieceId = PieceId()


