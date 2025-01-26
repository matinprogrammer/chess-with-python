from .abstract_piece import AbstractPiece
from typing import List
from ..tools import Position


class Queen(AbstractPiece):
    def get_all_moves(self) -> List[List[int]]:
        moves = [[], [], [], [], [], [], [], []]

        for i in range(1, 8):
            if pos := Position.get_pos_or_false_by_x_y(self.position.x + i, self.position.y):
                moves[0].append(pos)

        for i in range(1, 8):
            if pos := Position.get_pos_or_false_by_x_y(self.position.x + i, self.position.y + i):
                moves[1].append(pos)

        for i in range(1, 8):
            if pos := Position.get_pos_or_false_by_x_y(self.position.x, self.position.y + i):
                moves[2].append(pos)

        for i in range(1, 8):
            if pos := Position.get_pos_or_false_by_x_y(self.position.x - i, self.position.y + i):
                moves[3].append(pos)

        for i in range(1, 8):
            if pos := Position.get_pos_or_false_by_x_y(self.position.x - i, self.position.y):
                moves[4].append(pos)

        for i in range(1, 8):
            if pos := Position.get_pos_or_false_by_x_y(self.position.x - i, self.position.y - i):
                moves[5].append(pos)

        for i in range(1, 8):
            if pos := Position.get_pos_or_false_by_x_y(self.position.x, self.position.y - i):
                moves[6].append(pos)

        for i in range(1, 8):
            if pos := Position.get_pos_or_false_by_x_y(self.position.x + i, self.position.y - i):
                moves[7].append(pos)

        return moves
