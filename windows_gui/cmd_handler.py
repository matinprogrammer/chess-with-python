from core import Position, AbstractPiece, Pawn, King, Queen, Rook, Bishop, Knight, Chess
from typing import Union, List, Dict, Tuple


class InvalidAlgebraicNotation(ValueError):
    pass


class CmdHandler:
    charset_column = {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5, "f": 6, "g": 7, "h": 8}
    pieces_short = {"K": King, "D": Queen, "T": Rook, "L": Bishop, "R": Knight, "P": Pawn}

    def __init__(self, user_input: str):
        self.user_input = user_input

    def get_algebraic_notation(self) -> Dict:
        if len(self.user_input) == 2 or ("x" in self.user_input and len(self.user_input) == 3):
            self.user_input = "p" + self.user_input

        if len(self.user_input) < 3:
            raise InvalidAlgebraicNotation("invalid input")

        try:
            piece: str = self.user_input[0].upper()
            if piece not in self.pieces_short.keys():
                raise InvalidAlgebraicNotation("invalid piece you are input")
        except IndexError:
            raise InvalidAlgebraicNotation("dont enter zero len input")
        except Exception as e:
            raise InvalidAlgebraicNotation("invalid piece input") from e

        which_piece: Union[list, None] = None
        if len(self.user_input) > 3:
            try:
                if "x" in self.user_input:
                    which_piece = self.user_input[1: -3]
                else:
                    which_piece = self.user_input[1: -2]
            except Exception as e:
                raise InvalidAlgebraicNotation("invalid piece input") from e

        is_attack: bool = False
        if "x" in self.user_input:
            if "x" != self.user_input[-3]:
                raise InvalidAlgebraicNotation("invalid position of x")
            is_attack = True

        try:
            destination_move: str = self.user_input[-2:]
            if not destination_move[0].isascii():
                raise InvalidAlgebraicNotation(f"column input is wrong. column: {destination_move[0]}")
            if not destination_move[1].isnumeric():
                raise InvalidAlgebraicNotation(f"row input is wrong. row: {destination_move[1]}")
        except Exception as e:
            raise InvalidAlgebraicNotation(f"invalid destination move input") from e

        return {"piece": piece, "which_piece": which_piece, "destination_move": destination_move,
                "is_attack": is_attack}

    def get_piece_move_with_code(self, chess: Chess) -> Tuple:
        cell_id = 0
        algebraic_notation = {}
        result: Union[str, AbstractPiece] = "piece moved"
        status_code = 0

        try:
            algebraic_notation: Dict = self.get_algebraic_notation()
        except InvalidAlgebraicNotation as e:
            result = f"invalid input {str(e)}"
            status_code = 1

        if status_code == 0:
            cell_id = Position.get_real_position_by_x_y(
                int(algebraic_notation["destination_move"][1]),
                self.charset_column[algebraic_notation["destination_move"][0]]
            )
            pieces_list = []
            all_own_pieces: List[AbstractPiece] = chess.board.get_all_pieces_by_color()[chess.turn].values()
            for own_piece in all_own_pieces:
                if isinstance(own_piece, self.pieces_short[algebraic_notation["piece"]]):
                    all_moves = own_piece.get_real_moves(chess.board.get_all_pieces()).moves
                    all_attacks = (own_piece.get_real_attack(chess.board.get_all_pieces_by_color())
                                   .attacks)
                    if (
                            (not algebraic_notation["is_attack"] and cell_id in all_moves)
                            or (algebraic_notation["is_attack"] and cell_id in all_attacks)
                    ):
                        pieces_list.append(own_piece)

            if len(pieces_list) == 1:
                result = pieces_list[0]
            else:
                result = "invalid input"
        return status_code, result, cell_id, algebraic_notation["is_attack"]
