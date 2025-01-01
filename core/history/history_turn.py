from ..tools import Position
from ..pieces import AbstractPiece
from dataclasses import dataclass
from .move_status import MoveStatus
from utils.log import core_logger
from typing import List


class TurnError(ValueError):
    pass


@dataclass
class HistoryTurn:
    turn_number: int
    piece: AbstractPiece
    from_position: Position
    to_position: Position
    move_status: MoveStatus

    is_small_castling: bool
    is_big_castling: bool

    is_exchange: bool
    is_attack: bool
    is_check: bool
    is_double_check: bool
    is_stale_mate: bool
    is_check_mate: bool

    def __post_init__(self):
        self.validate_property()

        # log
        property_str = "-"
        for property_ in self.get_all_property():
            if getattr(self, property_):
                property_str += f"{property_}: {str(getattr(self, property_))}"
        core_logger.info(f"HistoryTurn with {str(property_str)} property initialised")

    def get_all_property(self) -> List[str]:
        return list(vars(self))

    def validate_property(self):
        # validate turn_number
        if self.turn_number < 1:
            raise TurnError("turn cant be less than 1")

        # validate piece
        if not isinstance(self.piece, AbstractPiece):
            raise TypeError("piece must be AbstractPiece")

        # validate from_position
        if not isinstance(self.from_position, Position):
            raise TypeError("from_position must be a Position")

        # validate to_position
        if not isinstance(self.to_position, Position):
            raise TypeError("to_position must be a Position")

        # validate move_status
        if not isinstance(self.move_status, MoveStatus):
            raise TypeError("move_status must be MoveStatus")

        # validate is_small_castling
        if not isinstance(self.is_small_castling, bool):
            raise TypeError("is_small_castling must be bool")

        # validate is_big_castling
        if not isinstance(self.is_big_castling, bool):
            raise TypeError("is_big_castling must be bool")

        # validate is_exchange
        if not isinstance(self.is_exchange, bool):
            raise TypeError("is_exchange must be bool")

        # validate is_attack
        if not isinstance(self.is_attack, bool):
            raise TypeError("is_attack must be bool")

        # validate is_check
        if not isinstance(self.is_check, bool):
            raise TypeError("is_check must be bool")

        # validate is_double_check
        if not isinstance(self.is_double_check, bool):
            raise TypeError("is_double_check must be bool")

        # validate is_stale_mate
        if not isinstance(self.is_stale_mate, bool):
            raise TypeError("is_stale_mate must be bool")

        # validate is_check_mate
        if not isinstance(self.is_check_mate, bool):
            raise TypeError("is_check_mate must be bool")

    def __repr__(self) -> str:
        return (f'{self.__class__.__name__}(turn_number={self.turn_number}, piece={self.piece},'
                f'from_position={self.from_position}, to_position={self.to_position}, move_status={self.move_status}')

    def __str__(self) -> str:
        return (f'piece {self.piece} from {self.from_position} {"attack to" if self.is_attack else "move to"} '
                f'to {self.to_position}')
