from .board import Board
from .history import History
from .pieces import King, PieceRequest, AbstractPiece
from .tools import Turn
from typing import Union, Dict
from utils.log import core_logger
import itertools


class Chess:
    def __init__(self) -> None:
        self.board = Board()
        self.turn = Turn(1)
        self.history: History = History()
        self.current_piece_request: PieceRequest = PieceRequest()

        self.game_start = True
        self.is_check = False
        self.is_check_mate = False

        self.check_position: Union[None, int] = None
        self.Which_piece_has_checked: Union[AbstractPiece, None] = None

        # log
        core_logger.info("Chess initialised")

    def get_own_pieces(self) -> Dict[int, AbstractPiece]:
        return self.board.get_all_pieces_by_color()[self.turn.turn_str]

    def get_opponent_pieces(self) -> Dict[int, AbstractPiece]:
        return self.board.get_all_pieces_by_color()[self.turn.reverse_turn_str]

    def get_own_king(self) -> King:
        if self.turn.turn_str == "white":
            return self.board.pw_king
        else:
            return self.board.pb_king

    def get_opponent_king(self) -> King:
        if self.turn.turn_str == "white":
            return self.board.pb_king
        else:
            return self.board.pw_king

    def get_is_check_with_piece_move(self, piece: AbstractPiece, move_cell_id: int) -> bool:
        piece.move(move_cell_id)
        is_check: bool = self.get_is_check(self.get_own_king())
        piece.position.return_to_last_position()
        return is_check

    def own_is_check(self) -> bool:
        return self.get_is_check(self.get_own_king())

    def opponent_is_check(self) -> bool:
        return self.get_is_check(self.get_opponent_king())

    def get_is_check(self, king: AbstractPiece) -> bool:
        is_check = False
        for piece in self.board.get_all_pieces_by_color()[king.color.opponent].values():
            attacks = (piece.get_real_attack(self.board.get_all_pieces_by_color())
                       .attacks)

            if king.position.get_real_position() in attacks:
                is_check = True

            if is_check:
                self.Which_piece_has_checked = piece
                break
        return is_check

    def own_is_check_mate(self) -> bool:
        return self.get_is_check_mate(self.get_own_king())

    def opponent_is_check_mate(self) -> bool:
        return self.get_is_check_mate(self.get_opponent_king())

    def get_is_check_mate(self, king: King) -> bool:
        all_pieces_bool = []
        # loop in own pieces
        for piece in self.board.get_all_pieces_by_color()[king.color.get()].values():
            all_piece_moves = piece.get_real_moves(self.board.get_all_pieces()).moves
            all_piece_attacks = piece.get_real_attack(self.board.get_all_pieces_by_color()).attacks

            moves_bool = list(itertools.repeat(False, len(all_piece_moves)))
            attacks_bool = list(itertools.repeat(False, len(all_piece_attacks)))
            all_moves_bool = moves_bool + attacks_bool

            for index, move in enumerate(all_piece_moves + attacks_bool):
                if index > len(all_piece_moves):
                    self.board.get_all_pieces().get(move).is_killed.set(True)
                piece.position.set_position(move)

                is_check = False
                for opponent_piece in self.board.get_all_pieces_by_color()[king.color.opponent].values():
                    attacks = (
                        opponent_piece.get_real_attack(self.board.get_all_pieces_by_color())
                        .attacks
                    )

                    if king.position.get_real_position() in attacks:
                        is_check = True

                all_moves_bool[index] = not is_check
                piece.position.return_to_last_position()
                if len(all_moves_bool) != 0:
                    all_pieces_bool.append(any(all_moves_bool))

        return not any(all_pieces_bool)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def __str__(self) -> str:
        return f"board in turn {self.turn.turn_str}"
