from .pieces import Rook, Knight, Bishop, King, Queen, WPawn, BPawn, AbstractPiece
from typing import List


class Board:
    def __init__(self) -> None:
        self.pwr_rook = Rook("white", 1, 8, "right")
        self.pwl_rook = Rook("white", 1, 1, "left")
        self.pwr_knight = Knight("white", 1, 7, "right")
        self.pwl_knight = Knight("white", 1, 2, "left")
        self.pwr_bishop = Bishop("white", 1, 6, "right")
        self.pwl_bishop = Bishop("white", 1, 3, "left")
        self.pw_king = King("white", 1, 5, None)
        self.pw_queen = Queen("white", 1, 4, None)
        self.pw_pawns = []
        for i in range(1, 9):
            self.pw_pawns.append(WPawn(i, "white", 2, i, None))

        self.pbr_rook = Rook("black", 8, 8, "right")
        self.pbl_rook = Rook("black", 8, 1, "left")
        self.pbr_knight = Knight("black", 8, 7, "right")
        self.pbl_knight = Knight("black", 8, 2, "left")
        self.pbr_bishop = Bishop("black", 8, 6, "right")
        self.pbl_bishop = Bishop("black", 8, 3, "left")
        self.pb_king = King("black", 8, 5, None)
        self.pb_queen = Queen("black", 8, 4, None)
        self.pb_pawns = []
        for i in range(1, 9):
            self.pb_pawns.append(BPawn(i, "black", 7, i, None))

    @property
    def white_pieces(self) -> List[AbstractPiece]:
        return [
            self.pwr_rook,
            self.pwl_rook,
            self.pwr_knight,
            self.pwl_knight,
            self.pwr_bishop,
            self.pwl_bishop,
            self.pw_king,
            self.pw_queen,
            *self.pw_pawns
        ]

    @property
    def black_pieces(self) -> List[AbstractPiece]:
        return [
            self.pbr_rook,
            self.pbl_rook,
            self.pbr_knight,
            self.pbl_knight,
            self.pbr_bishop,
            self.pbl_bishop,
            self.pb_king,
            self.pb_queen,
            *self.pb_pawns
        ]

    @property
    def all_pieces(self) -> List[AbstractPiece]:
        return [
            *self.white_pieces,
            *self.black_pieces
        ]

    def get_white_pieces(self):
        return {piece.position.get_real_position(): piece for piece in self.white_pieces if not piece.is_killed}

    def get_black_pieces(self):
        return {piece.position.get_real_position(): piece for piece in self.black_pieces if not piece.is_killed}

    def get_all_pieces(self):
        return {**self.get_white_pieces(), **self.get_black_pieces()}

    def get_all_pieces_by_color(self):
        return {"white": {**self.get_white_pieces()}, "black": {**self.get_black_pieces()}}

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def __str__(self) -> str:
        return repr(self)
