from abc import ABC
from core.tools import Position, Path


class PieceColor:
    pass


class PieceIsKilled:
    pass


class PieceDirection:
    pass


class PieceId:
    pass


class AbstractPieces(ABC):
    def __init__(self) -> None:
        self.position: Position = Position()
        self.picture_path: Path = Path()
        self.color: PieceColor = PieceColor()
        self.is_killed: PieceIsKilled = PieceIsKilled()
        self.direction: PieceDirection = PieceDirection()
        self.id: PieceId = PieceId()

    
