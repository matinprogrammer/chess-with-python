from core import Chess
from core import (AbstractPiece, PieceRequest, Position, HistoryTurn, MoveStatus, Pawn, Queen, Bishop, Rook, Knight)
from typing import Union, List, Optional
import threading
import tkinter
import functools
from .utils import ChessCell, ChessLabel, set_label_image, remove_label_image
from .cmd_handler import CmdHandler, CmdRequest, InvalidAlgebraicNotation, InvalidMove


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

        self.window = tkinter.Tk()
        self.window.title("Chessboard")
        self.window.resizable(False, False)
        self.window.geometry(f"480x480+1010+180")
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.chess = chess

        self.main_frame: Union[None, tkinter.Frame] = None
        self.cells: List[Optional[ChessCell]] = []
        self.cells_label: List[Optional[ChessLabel]] = []

        self.pieces_request: List[PieceRequest] = []
        self.data: PieceRequest = PieceRequest()

        input_thread = threading.Thread(target=self.get_input, daemon=True, args=[None])
        input_thread.start()

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

    def get_input(self, result: Union[str, None]):
        while True:
            if result is not None:
                print(result)

            user_input = input(">> ")

            if user_input == "q":
                self.window.destroy()

            if user_input == "r":
                self.restart_game()
                continue

            try:
                cmd_request: CmdRequest = CmdHandler(user_input).get_piece_move_with_code(self.chess)
            except (InvalidMove, InvalidAlgebraicNotation) as e:
                print(str(e))
                continue

            self.set_data_to_null()
            if cmd_request.piece is not None:
                self.set_moves_attacks(cmd_request.piece)
                self.set_piece_move(self.data, cmd_request.destination_move_position, is_attack=cmd_request.is_attack)
            else:
                print("invalid input")

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
        if piece is not None:
            self.pieces_request.insert(0, self.data)

    def set_piece_move(
            self, piece_request: PieceRequest, cell_id: int, *, increase_turn=True, is_attack=False
    ) -> None:
        if is_attack:
            witch_move = piece_request.attacks.index(cell_id)

            last_cell_id: int = piece_request.attack_from_to_position[witch_move][0]
            current_cell_id: int = piece_request.attacks[witch_move]
            self.remove_piece_from_board(piece_request.attack_from_to_position[witch_move][1])

            piece_request.oppoonent_pieces[witch_move].is_killed.set(True)
        else:
            witch_move = piece_request.moves.index(cell_id)

            last_cell_id: int = piece_request.move_from_to_position[witch_move][0]
            current_cell_id: int = piece_request.moves[witch_move]

        piece = piece_request.piece

        if self.chess.get_is_check_with_piece_move(piece, cell_id):
            return None
        else:
            self.chess.is_check = False
            self.chess.check_position = None
            self.chess.Which_piece_has_checked = None

        self.change_piece_position_in_board(piece, last_cell_id, current_cell_id)

        is_small_castling = False
        is_big_castling = False

        if hasattr(piece, "is_move"):
            piece.is_move.set(True)

        if isinstance(pawn := piece, Pawn):
            if pawn.color == "black" and pawn.position.x == 1:
                self.upgrade_pawn(pawn)
            elif pawn.color == "white" and pawn.position.x == 8:
                self.upgrade_pawn(pawn)

        if piece_request.is_small_castling or piece_request.is_big_castling:
            try:
                rook = piece_request.castle_rooks[cell_id + 1]
            except KeyError:
                rook = piece_request.castle_rooks[cell_id - 2]
            rook_position = rook.position.get_real_position()

            if rook.direction == "right":
                is_small_castling = True
                self.change_piece_position_in_board(rook, rook_position, rook_position - 2)
            elif rook.direction == "left":
                is_big_castling = True
                self.change_piece_position_in_board(rook, rook_position, rook_position + 3)

        if self.chess.opponent_is_check():
            self.chess.is_check = True
            self.chess.check_position = self.chess.get_opponent_king().position.get_real_position()
            if self.chess.opponent_is_check_mate():
                self.chess.is_check_mate = True
                self.chess.game_start = False

        self.chess.history.append(
            HistoryTurn(
                turn_number=self.chess.turn.turn_number,
                piece=piece,
                from_position=Position(last_cell_id),
                to_position=Position(current_cell_id),
                move_status=MoveStatus(),
                is_attack=is_attack,
                is_small_castling=is_small_castling,
                is_big_castling=is_big_castling,
                is_check=self.chess.is_check,
                is_check_mate=self.chess.is_check_mate,
            )
        )
        self.set_data_to_null()
        if increase_turn:
            self.chess.turn.increase_turn()

    def upgrade_pawn(self, pawn):
        self.chess.game_start = False
        popup = tkinter.Toplevel(self.window)
        popup.title("choose your pawn")
        popup.geometry("250x60+400+300")
        board_popup = tkinter.Frame(popup)
        board_popup.grid(row=0, column=0)
        list_on_piece = [
            Bishop(pawn.color, pawn.position.x, pawn.position.y, None),
            Knight(pawn.color, pawn.position.x, pawn.position.y, None),
            Rook(pawn.color, pawn.position.x, pawn.position.y, None),
            Queen(pawn.color, pawn.position.x, pawn.position.y, None)
        ]
        for index, piece in enumerate(list_on_piece):
            label = ChessLabel(0, popup)
            set_label_image(label, piece.picture_path.get())
            label.grid(row=0, column=index)
            label.bind(f"<Button-1>", functools.partial(self.upgrade_pawn_click, popup=popup, pawn=pawn, piece=piece))

    def upgrade_pawn_click(self, event, popup: tkinter.Toplevel, pawn: Pawn, piece: AbstractPiece):
        self.chess.game_start = True
        cell_id = pawn.position.get_real_position()
        self.remove_piece_from_board(cell_id)
        self.add_piece_in_board(cell_id, piece)
        if pawn.color == "white":
            self.chess.board.pw_pawns[pawn.id - 1] = piece
        else:
            self.chess.board.pb_pawns[pawn.id - 1] = piece
        popup.destroy()

        if self.chess.own_is_check():
            self.chess.is_check = True
            self.chess.check_position = self.chess.get_own_king().position.get_real_position()
            if self.chess.opponent_is_check_mate():
                self.chess.is_check_mate = True
        self.set_chess_board_colors()

    def change_piece_position_in_board(self, piece, last_cell_id, current_cell_id) -> None:
        self.remove_piece_from_board(last_cell_id)
        self.add_piece_in_board(current_cell_id, piece)

    def remove_piece_from_board(self, cell_id: int):
        remove_label_image(self.cells_label[cell_id - 1])
        self.cells_label[cell_id - 1].bind(
            f"<Button-1>",
            functools.partial(self.on_cell_click, cell_id=cell_id, piece=None)
        )

    def add_piece_in_board(self, cell_id: int, piece: AbstractPiece):
        set_label_image(self.cells_label[cell_id - 1], piece.picture_path.get())
        self.cells_label[cell_id - 1].bind(
            f"<Button-1>",
            functools.partial(self.on_cell_click, cell_id=cell_id, piece=piece)
        )
        piece.move(cell_id)

    def set_moves_attacks(self, piece: AbstractPiece) -> None:
        if piece is not None:
            pr = PieceRequest()
            pr += piece.get_real_moves(self.chess.board.get_all_pieces())
            get_real_attack = piece.get_real_attack
            if isinstance(piece, Pawn):
                get_real_attack = functools.partial(piece.get_real_attack, history=self.chess.history)
            pr += get_real_attack(self.chess.board.get_all_pieces_by_color())
            self.data = pr

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

    def restart_game(self, event=None) -> None:
        for widget in self.window.winfo_children():
            widget.destroy()
        self.cells = []
        self.cells_label = []
        self.chess = Chess()
        self.set_data_to_null()
        self.create_chess_board()

    def show(self) -> None:
        self.window.mainloop()

    def on_closing(self):
        self.window.destroy()
