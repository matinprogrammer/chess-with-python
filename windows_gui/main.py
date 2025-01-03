from core import Chess
from core import (AbstractPiece, PieceRequest, Position, History, HistoryTurn, MoveStatus, Pawn,
                  Rook, Knight, Bishop, Queen, King)
from typing import Union, List, Optional, Callable
from utils.log import windows_gui_logger
import threading
import tkinter
import functools
from .utils import ChessCell, ChessLabel, set_label_image, remove_label_image
from .funcs import get_window_gui
from .cmd_handler import CmdHandler


class WindowsGui:
    cell_colors = {
        "normal": ["#A66D4F", "#DDB88C"],
        "move": "#00FF00",
        "attack": "#FF0000",
        "check": "#ff9900",
    }

    def __init__(self, chess: 'Chess'):
        with open("logs/core.log", "w") as f:
            f.write("")

        self.window = get_window_gui(self.on_closing)
        self.chess = chess

        self.main_frame: Union[None, tkinter.Frame] = None
        self.cells: List[Optional[ChessCell]] = []
        self.cells_label: List[Optional[ChessLabel]] = []

        self.pieces_request: List[PieceRequest] = []
        self.data: PieceRequest = PieceRequest()

    def set_data_to_null(self):
        self.data = PieceRequest()

    def create_chess_board(self):
        gui_board = tkinter.Frame(self.window)
        gui_board.grid(row=0, column=0)
        self.window.bind('<Control-r>', self.restart_game)

        for row in range(1, 9):
            for col in range(1, 9):
                real_id = (row - 1) * 8 + col

                cell = ChessCell(real_id, gui_board, width=60, height=60)
                cell.grid(row=8 - row, column=col - 1)
                cell.pack_propagate(False)

                label = ChessLabel(real_id, cell, width=60, height=60)
                current_piece: Union[None, AbstractPiece] = None

                if label.id in self.chess.board.get_all_pieces().keys():
                    current_piece = self.chess.board.get_all_pieces()[label.id]
                    set_label_image(label, current_piece.picture_path.path)

                label.pack()
                label.bind(f"<Button-1>", functools.partial(self.on_cell_click, cell_id=real_id, piece=current_piece))

                self.cells.append(cell)
                self.cells_label.append(label)

        self.main_frame = gui_board
        self.set_chess_board_colors()

        input_thread = threading.Thread(target=self.get_input, daemon=True, args=[None])
        input_thread.start()

    def get_input(self, result: Union[str, None]):
        if result is not None:
            print(result)
        user_input = input(">> ")
        if user_input == "q":
            self.window.destroy()
        result = CmdHandler(user_input).get_piece_move_with_code(self.chess)
        if result[0] != 0:
            print(result[1])
        else:
            self.set_data_to_null()
            self.set_moves_attacks(result[1])
            self.set_piece_move(result[2], is_attack=result[3])

    def on_cell_click(self, event, cell_id: int, piece: Union[None, AbstractPiece]):
        all_pieces_data = ""
        for key, value in self.chess.board.get_all_pieces().items():
            all_pieces_data += f"\n\t{key} is {str(value)}"

        if not self.chess.game_start:
            return

        if hasattr(piece, "color") and piece.color.get() != self.chess.turn.turn_str:
            piece = None

        if cell_id in self.data.moves:
            self.set_piece_move(self.pieces_request[0], cell_id)
        elif cell_id in self.data.attacks:
            self.set_piece_move(self.pieces_request[0], cell_id, is_attack=True)
        else:
            self.set_data_to_null()
            self.set_moves_attacks(piece)

        self.set_chess_board_colors()
        # if piece is not None:
        #     self.pieces_request.insert(0, self.chess.piece_request)

    def set_moves_attacks(self, piece: AbstractPiece) -> None:
        if piece is not None:
            pr = PieceRequest()
            pr += piece.get_real_moves(self.chess.board.get_all_pieces())
            get_real_attack = piece.get_real_attack
            if isinstance(piece, Pawn):
                get_real_attack = functools.partial(piece.get_real_attack, history=self.chess.history)
            pr += get_real_attack(self.chess.board.get_all_pieces_by_color())
            self.data = pr

    def show(self) -> None:
        self.window.mainloop()

    def set_chess_board_colors(self) -> None:
        if self.main_frame is None:
            raise RuntimeError("cant set chess board colors with out use create chess board")
        if self.cells is None:
            raise RuntimeError("the cells list is not set")
        if self.cells_label is None:
            raise RuntimeError("the cells label list is not set")

        for label in self.cells_label:
            if label.id in self.data.moves:
                color = self.cell_colors["move"]
            elif label.id in self.data.attacks:
                color = self.cell_colors["attack"]
            elif label.id == self.chess.check_position:
                color = self.cell_colors["check"]
            else:
                color = self.cell_colors["normal"][sum(Position.get_x_y_from_position(label.id)) % 2]
            label.config(bg=color)

    def restart_game(self, event):
        for widget in self.window.winfo_children():
            widget.destroy()
        self.cells = []
        self.cells_label = []
        self.chess = Chess()
        self.create_chess_board()

    def on_closing(self):
        self.window.destroy()
