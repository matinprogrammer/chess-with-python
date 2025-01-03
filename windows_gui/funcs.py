import tkinter
from typing import Callable, Union, Tuple
from .utils import set_label_image, ChessLabel, ChessCell
from core import AbstractPiece, Chess
import functools


def get_window_gui(on_closing_func: Callable) -> tkinter.Tk:
    window = tkinter.Tk()
    window.title("Chessboard")
    window.resizable(False, False)
    window.geometry(f"480x480+700+200")
    window.protocol("WM_DELETE_WINDOW", on_closing_func)
    return window
