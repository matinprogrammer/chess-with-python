from .abstract_piece import AbstractPiece
from typing import List
from ..tools import Position


class Bishop(AbstractPiece):
    def __init__(self, *args) -> None:
        super().__init__(*args)
        self.picture_path /= "bishop.png"

    def get_all_moves(self) -> List[List[int]]:
        moves = [[], [], [], []]

        for i in range(1, 8):
            if pos := Position.get_pos_or_false_by_x_y(self.position.x + i, self.position.y + i):
                moves[0].append(pos)

        for i in range(1, 8):
            if pos := Position.get_pos_or_false_by_x_y(self.position.x - i, self.position.y + i):
                moves[1].append(pos)

        for i in range(1, 8):
            if pos := Position.get_pos_or_false_by_x_y(self.position.x - i, self.position.y - i):
                moves[2].append(pos)

        for i in range(1, 8):
            if pos := Position.get_pos_or_false_by_x_y(self.position.x + i, self.position.y - i):
                moves[3].append(pos)

        return moves
