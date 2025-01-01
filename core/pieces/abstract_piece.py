from abc import ABC
from os import getcwd
from ..tools import Position, Path
from ..tools.pieces import PieceColor, PieceDirection, PieceId, PieceIsKilled, PieceIsMoved
from typing import Dict


class AbstractPiece(ABC):
    def __init__(self, pos_x: int, pos_y: int, color: str, direction: str) -> None:
        self.position: Position = Position(pos_x, pos_y)
        self.color: PieceColor = PieceColor(color)
        self.direction: PieceDirection = PieceDirection(direction)
        self.picture_path: Path = Path(f"{getcwd()}\\media\\images\\pieces\\{str(self.color)}")
        self.is_killed: PieceIsKilled = PieceIsKilled(False)
        self.is_move = PieceIsMoved(False)
        self.id: PieceId = PieceId()

    @staticmethod
    def check_valid_pieces(pieces: Dict[int, 'AbstractPieces']) -> None:
        if not all(isinstance(piece, AbstractPiece) for piece in pieces.values()):
            raise ValueError(f"the all of pieces must be instance of pieces")

        for piece_key, piece_value in pieces.items():
            if piece_key != piece_value.position.get_real_position():
                raise ValueError(f"pieces key must be piece real position")

