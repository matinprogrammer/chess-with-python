from abc import ABC, abstractmethod
from ..tools import Position, Path
from ..tools.pieces import PieceColor, PieceDirection, PieceId, PieceIsKilled, PieceIsMoved
from typing import Dict, List, Optional, Union
from .piece_request import PieceRequest
import itertools, os
from utils.log import core_logger


class AbstractPiece(ABC):
    def __init__(self, color: str, pos_x: int, pos_y: int, direction: Union[str, None]) -> None:
        self.position: Position = Position(pos_x, pos_y)
        self.color: PieceColor = PieceColor(color)
        self.direction: PieceDirection = PieceDirection(direction)
        self.picture_path: Path = (
            Path(f"{os.getcwd()}\\media\\images\\pieces\\{str(self.color)}{self.__class__.__name__}.png")
        )
        self.is_killed: PieceIsKilled = PieceIsKilled(False)
        self.is_move = PieceIsMoved(False)
        self.id: PieceId = PieceId()

        # log
        core_logger.info(f"Piece {self.__class__.__name__} initialised")

    def get_real_moves(self, pieces: Dict[int, 'AbstractPiece']) -> PieceRequest:
        self.check_valid_pieces(pieces)
        moves: List[Optional[int]] = []
        for align_moves in self.get_all_moves():
            for move in align_moves:
                if move not in pieces.keys():
                    moves.append(move)
                else:
                    break

        return PieceRequest(
            piece=self,
            moves=moves,
            move_from_position=list(itertools.repeat(self.position.get_real_position(), len(moves))),
            move_to_position=moves
        )

    def get_real_attack(self, pieces_color: Dict[str, Dict[int, 'AbstractPiece']]) -> PieceRequest:
        colors = {"white": 1, "black": 1}
        for color in pieces_color.keys():
            if color in colors.keys():
                colors[color] -= 1

        if not all([color == 0 for color in colors.values()]):
            raise ValueError("pieces_color keys must be white and black")

        self.check_valid_pieces({**pieces_color["white"], **pieces_color["white"]})

        attacks: Optional[List[int], List] = []
        attack_pieces: List['AbstractPiece'] = []

        for align_moves in self.get_all_moves():
            for move in align_moves:
                if move in pieces_color[str(self.color)].keys():
                    break

                if move in pieces_color[self.color.opponent].keys():
                    attacks.append(move)
                    attack_pieces.append(pieces_color[self.color.opponent][move])
                    break

        return PieceRequest(
            piece=self,
            oppoonent_pieces=attack_pieces,
            attacks=attacks,
            attack_from_position=list(itertools.repeat(self.position.get_real_position(), len(attacks))),
            attack_to_position=attacks
        )

    @abstractmethod
    def get_all_moves(self) -> List[List[int]]:
        pass

    @staticmethod
    def check_valid_pieces(pieces: Dict[int, 'AbstractPiece']) -> None:
        if not all(isinstance(piece, AbstractPiece) for piece in pieces.values()):
            raise ValueError(f"the all of pieces must be instance of pieces")

        for piece_key, piece_value in pieces.items():
            if piece_key != piece_value.position.get_real_position():
                raise ValueError(f"pieces key must be piece real position")

    def __repr__(self) -> str:
        return (
            f"Piece {self.__class__.__name__}"
            f"(color={self.color}, "
            f"pos_x={self.position.x}, "
            f"pos_x={self.position.x}, "
            f"picture_path={str(self.picture_path)}, "
            f"is_killed={self.is_killed})"
        )

    def __str__(self) -> str:
        return (
            f"price {self.color} {self.__class__.__name__} in {self.position.x}X{self.position.y} "
            f"{'died' if self.is_killed else 'alive'}"
        )
