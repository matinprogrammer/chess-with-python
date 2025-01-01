from .abstract_piece import AbstractPiece
from .piece_request import PieceRequest
from typing import List, Dict, Optional
from ..tools import Position
from .rook import Rook
import itertools


class King(AbstractPiece):
    def __init__(self, *args) -> None:
        super().__init__(*args)
        self.picture_path /= "king.png"

    def get_all_moves(self) -> List[List[int]]:
        moves = []

        if pos := Position.get_pos_or_false_by_x_y(self.position.x + 1, self.position.y):
            moves.append([pos])

        if pos := Position.get_pos_or_false_by_x_y(self.position.x + 1, self.position.y + 1):
            moves.append([pos])

        if pos := Position.get_pos_or_false_by_x_y(self.position.x, self.position.y + 1):
            moves.append([pos])

        if pos := Position.get_pos_or_false_by_x_y(self.position.x - 1, self.position.y + 1):
            moves.append([pos])

        if pos := Position.get_pos_or_false_by_x_y(self.position.x - 1, self.position.y):
            moves.append([pos])

        if pos := Position.get_pos_or_false_by_x_y(self.position.x - 1, self.position.y - 1):
            moves.append([pos])

        if pos := Position.get_pos_or_false_by_x_y(self.position.x, self.position.y - 1):
            moves.append([pos])

        if pos := Position.get_pos_or_false_by_x_y(self.position.x + 1, self.position.y - 1):
            moves.append([pos])

        return moves

    # override for add castling
    def get_real_moves(self, pieces: Dict[int, AbstractPiece]) -> PieceRequest:
        self.check_valid_pieces(pieces)
        king_real_position = self.position.get_real_position()

        is_big_castling = False
        is_small_castling = False
        rooks: Dict[int, AbstractPiece] = {}

        moves: List[Optional[int]] = []
        for align_moves in self.get_all_moves():
            for move in align_moves:
                if move not in pieces.keys():
                    moves.append(move)
                else:
                    break

        # castling
        if not self.is_move:
            right_rook = pieces.get(king_real_position + 3)
            left_rook = pieces.get(king_real_position - 4)

            if isinstance(right_rook, Rook) and not right_rook.is_move:
                if pieces.get(king_real_position + 1) is None and pieces.get(king_real_position + 2) is None:
                    moves.append(king_real_position + 2)
                    rooks[right_rook.position.get_real_position()] = right_rook
                    is_small_castling = True

            if isinstance(left_rook, Rook) and not left_rook.is_move:
                if (
                        pieces.get(king_real_position - 1) is None
                        and pieces.get(king_real_position - 2) is None
                        and pieces.get(king_real_position - 2) is None
                ):
                    moves.append(king_real_position - 2)
                    rooks[left_rook.position.get_real_position()] = left_rook
                    is_big_castling = True
        # end castling

        return PieceRequest(
            piece=self,
            is_small_castling=is_small_castling,
            is_big_castling=is_big_castling,
            moves=moves,
            move_from_position=list(itertools.repeat(self.position.get_real_position(), len(moves))),
            move_to_position=moves,
            castle_rooks=rooks
        )
