from core import Chess
from core import (AbstractPiece, PieceRequest, Position, History, HistoryTurn, MoveStatus, Pawn,
                  Rook, Knight, Bishop, Queen, King)
from typing import Union, List, Optional, Callable
from utils.log import windows_gui_logger
import itertools, functools, threading, tkinter
from .utils.widgets import ChessCell, ChessLabel
from .funcs import get_window_gui


class WindowsGui:
    cell_colors = {
        "normal": ["#A66D4F", "#DDB88C"],
        "move": "#00FF00",
        "attack": "#FF0000",
        "check": "#ff9900",
    }
    charset_column = {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5, "f": 6, "g": 7, "h": 8}
    pieces_short = {"K": King, "D": Queen, "T": Rook, "L": Bishop, "R": Knight, "P": Pawn}

    def __init__(self, chess: 'Chess'):
        with open("logs/core.log", "w") as f:
            f.write("")

        self.window = get_window_gui(self.on_closing)
        self.chess = chess

        self.main_frame: Union[None, tkinter.Frame] = None
        self.cells: List[Optional[ChessCell]] = []
        self.cells_label: List[Optional[ChessLabel]] = []

        self.pieces_request: List[PieceRequest] = []

