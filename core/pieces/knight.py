from .abstract_piece import AbstractPiece
from typing import List
from ..tools import Position


class Knight(AbstractPiece):
    def __init__(self, *args) -> None:
        super().__init__(*args)
        self.picture_path /= "knight.png"

    def get_all_moves(self) -> List[List[int]]:
        moves = []
        if pos := Position.get_pos_or_false_by_x_y(self.position.x + 2, self.position.y + 1):
            moves.append([pos])

        if pos := Position.get_pos_or_false_by_x_y(self.position.x + 1, self.position.y + 2):
            moves.append([pos])

        if pos := Position.get_pos_or_false_by_x_y(self.position.x - 1, self.position.y + 2):
            moves.append([pos])

        if pos := Position.get_pos_or_false_by_x_y(self.position.x - 2, self.position.y + 1):
            moves.append([pos])

        if pos := Position.get_pos_or_false_by_x_y(self.position.x - 1, self.position.y - 2):
            moves.append([pos])

        if pos := Position.get_pos_or_false_by_x_y(self.position.x - 2, self.position.y - 1):
            moves.append([pos])

        if pos := Position.get_pos_or_false_by_x_y(self.position.x + 1, self.position.y - 2):
            moves.append([pos])

        if pos := Position.get_pos_or_false_by_x_y(self.position.x + 2, self.position.y - 1):
            moves.append([pos])

        return moves
