from .board import Board
from .history import History
from .pieces import King, PieceRequest
from .tools import Turn


class Chess:
    def __init__(self) -> None:
        self.board = Board()
        self.turn = Turn(1)
        self.history: History = History()
        self.current_piece_request: PieceRequest = PieceRequest()

    def set_data_to_null(self):
        self.current_piece_request = PieceRequest()

    def get_own_king(self) -> King:
        if self.turn_str == "white":
            return self.board.pw_king
        else:
            return self.board.pb_king

    def get_opponent_king(self) -> King:
        if self.turn_str == "white":
            return self.board.pb_king
        else:
            return self.board.pw_king

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def __str__(self) -> str:
        return f"board in turn {self.turn_str}"