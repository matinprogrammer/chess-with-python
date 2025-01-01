import tkinter
from typing import Callable


def get_window_gui(on_closing_func: Callable):
    window = tkinter.Tk()
    window.title("Chessboard")
    window.resizable(False, False)
    window.geometry(f"480x480+700+200")
    window.protocol("WM_DELETE_WINDOW", on_closing_func)
