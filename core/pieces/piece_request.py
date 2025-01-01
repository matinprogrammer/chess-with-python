from dataclasses import dataclass, field, replace
from typing import Union, List, Dict, Optional, Tuple
from .abstract_piece import AbstractPiece
from ..tools.position import Position, PositionError
from utils.tools import is_instance_list


class PieceRequestError(Exception):
    pass


@dataclass
class PieceRequest:
    """
    this class is returned by get_real_move and get_real_attack of pieces
    """
    piece: AbstractPiece = None
    oppoonent_pieces: List[AbstractPiece] = field(default_factory=list)
    castle_rooks: Union[None, Dict[int, AbstractPiece]] = None
    moves: List[Optional[int]] = field(default_factory=list)
    attacks: List[Optional[int]] = field(default_factory=list)
    move_from_position: List[int] = field(default_factory=list)
    move_to_position: List[int] = field(default_factory=list)
    attack_from_position: List[int] = field(default_factory=list)
    attack_to_position: List[int] = field(default_factory=list)
    is_big_castling: bool = False
    is_small_castling: bool = False
    is_enpassant: bool = False
    is_empty: bool = False

    def __post_init__(self):
        self.validate_property()

    @property
    def move_from_to_position(self) -> List[Tuple[int]]:
        if len(self.move_from_position) != len(self.move_to_position) != len(self.moves):
            raise ValueError(f"Length of moves and positions do not match moves={self.moves} "
                             f"positions = {self.move_from_position} => {self.move_to_position}")
        return list(zip(self.move_from_position, self.move_to_position))

    @property
    def attack_from_to_position(self) -> List[Tuple[int]]:
        if len(self.attack_from_position) != len(self.attack_to_position) != len(self.attacks):
            raise ValueError(f"Length of moves and positions do not match attacks={self.attacks} "
                             f"positions = {self.attack_from_position} => {self.attack_to_position}")
        return list(zip(self.attack_from_position, self.attack_to_position))

    def __call__(self, **kwargs) -> 'PieceRequest':
        """
        this method return a new object of PiecesRequest(self) with all necessary
        :param kwargs: it is param of PiecesRequest(self)
        :return: new object of PiecesRequest(self)
        """
        return replace(self, **kwargs)

    def get_all_property(self) -> List[str]:
        properties = vars(self)
        # Include properties defined with @property decorator
        properties.update({
            "move_from_to_position": self.move_from_to_position,
            "attack_from_to_position": self.attack_from_to_position,
        })
        return list(properties)

    def validate_property(self) -> bool:
        # validate piece
        if self.piece and not isinstance(self.piece, AbstractPiece):
            raise PieceRequestError("Piece is not an AbstractPieces")

        # validate oppoonent_pieces
        if self.oppoonent_pieces:
            if not is_instance_list(self.oppoonent_pieces, AbstractPiece):
                raise PieceRequestError(f"opponent piece is not an AbstractPieces")

        # validate castle_rooks
        if self.castle_rooks:
            for piece_position, piece in self.castle_rooks.items():
                if not isinstance(piece, AbstractPiece):
                    raise PieceRequestError(f"piece in castle_rooks {piece} is not an AbstractPieces")
                if not isinstance(piece_position, int):
                    raise PieceRequestError("piece_id in castle_rooks is not and integer")
                try:
                    Position(piece_position)
                except PositionError as e:
                    raise PieceRequestError("piece_id in castle_rooks is not valid position") from e

        # validate moves
        if self.moves and not is_instance_list(self.moves, int):
            raise PieceRequestError("moves is not an int")

        # validate attacks
        if self.attacks and not is_instance_list(self.attacks, int):
            raise PieceRequestError("attacks is not correct set")

        # validate move_from_position
        if self.move_from_position and not is_instance_list(self.move_from_position, int):
            raise PieceRequestError("move_from_position is not correct set")

        # validate move_to_position
        if self.move_to_position and not is_instance_list(self.move_to_position, int):
            raise PieceRequestError("move_to_position is not correct set")

        # validate attack_from_position
        if self.attack_from_position and not is_instance_list(self.attack_from_position, int):
            raise PieceRequestError("attack_from_position is not correct set")

        # validate attack_to_position
        if self.attack_to_position and not is_instance_list(self.attack_to_position, int):
            raise PieceRequestError("attack_to_position is not correct set")

        # validate is_big_castling
        if not isinstance(self.is_big_castling, bool):
            raise PieceRequestError("is_big_castling is not a boolean")

        # validate is_small_castling
        if not isinstance(self.is_small_castling, bool):
            raise PieceRequestError("is_small_castling is not a boolean")

        # validate is_enpassant
        if not isinstance(self.is_enpassant, bool):
            raise PieceRequestError("is_enpassant is not a boolean")

        # validate is_empty
        if not isinstance(self.is_empty, bool):
            raise PieceRequestError("is_empty is not a boolean")

        return True

    def __str__(self) -> str:
        property_list = []
        for property_ in self.get_all_property():
            property_list.append(f"{property_.replace("_", " ")}: "
                                 f"{str(getattr(self, property_))}")
        return "\n".join(property_list)
