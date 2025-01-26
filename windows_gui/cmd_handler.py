from core import Position, AbstractPiece, Pawn, King, Queen, Rook, Bishop, Knight, Chess
from typing import Union, Dict, Tuple
from dataclasses import dataclass


class InvalidAlgebraicNotation(ValueError):
    pass


class InvalidMove(ValueError):
    pass


@dataclass
class CmdRequest:
    status_code: int
    message: str
    piece: AbstractPiece
    which_piece_position: int
    destination_move_position: int
    is_attack: bool = False
    is_big_castling: bool = False
    is_small_castling: bool = False
    is_double_check: bool = False
    is_check: bool = False
    is_check_mate: bool = False


class CmdHandler:
    charset_column = {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5, "f": 6, "g": 7, "h": 8}
    pieces_short = {"K": King, "D": Queen, "T": Rook, "L": Bishop, "R": Knight, "P": Pawn}
    # attack: x
    # check: +
    # double check: ++
    # check mate: #
    # small castling 0-0
    # big castling 0-0-0

    def __init__(self, user_input: str):
        self.user_input = user_input

    # sample:
        # a3 > pa3: pawn 1 3
        # rc3 > rc3: knight-1-2 3 3
        # rxc3 > rc3: knight-1-2 3 3 attack
        # rg3xc3 > rc3: knight-7-3 3 3 attack
        # rc3+ > rc3: knight-1-2 3 3 check
        # rc3# > rc3: knight-1-2 3 3 check_mate
        # 0-0 > 0-0: king small_castling
        # 0-0-0 > 0-0-0: king big_castling
    def get_algebraic_notation(self) -> Dict:
        is_big_castling = False
        is_small_castling = False
        is_attack = False
        is_double_check = False
        is_check = False
        is_check_mate = False
        piece: Union[None, AbstractPiece] = None
        which_piece_position: Union[None, str] = None
        destination_move_x_y: Union[None, Tuple[int, int]] = None

        if self.user_input == "0-0-0":
            is_big_castling = True
        if self.user_input == "0-0":
            is_small_castling = True
        if "x" in self.user_input:
            is_attack = True
        if "#" in self.user_input:
            is_check_mate = True
        if self.user_input.endswith("++"):
            is_double_check = True
        if self.user_input.endswith("+"):
            is_check = True

        if not is_small_castling and not is_big_castling:
            new_user_input = ""
            for string in self.user_input:
                if string not in ["0", "-", "+", "x", "#"]:
                    new_user_input += string

            if len(new_user_input) == 2:
                new_user_input = "p" + new_user_input

            if len(new_user_input) < 3:
                raise InvalidAlgebraicNotation("invalid input you must need enter another data to move")

            try:
                piece: str = new_user_input[0].upper()
                if piece not in self.pieces_short.keys():
                    raise InvalidAlgebraicNotation("invalid piece you are input")
            except IndexError:
                raise InvalidAlgebraicNotation("dont enter zero len input")
            except Exception as e:
                raise InvalidAlgebraicNotation("invalid piece input") from e

            which_piece_position: Union[str, None] = None
            if len(new_user_input) > 3:
                try:
                    which_piece_position = new_user_input[1: -2]
                except Exception as e:
                    raise InvalidAlgebraicNotation("invalid select piece input") from e

            try:
                destination_move_x_y: str = new_user_input[-2:]
                if not destination_move_x_y[0].isascii():
                    raise InvalidAlgebraicNotation(f"column input is wrong. column: {destination_move_x_y[0]}")
                if not destination_move_x_y[1].isnumeric():
                    raise InvalidAlgebraicNotation(f"row input is wrong. row: {destination_move_x_y[1]}")
            except Exception as e:
                raise InvalidAlgebraicNotation(f"invalid destination move input") from e

        return {
            "piece": piece,
            "which_piece_position": which_piece_position,
            "destination_move_x_y": destination_move_x_y,
            "is_attack": is_attack,
            "is_check": is_check,
            "is_double_check": is_double_check,
            "is_check_mate": is_check_mate,
            "is_small_castling": is_small_castling,
            "is_big_castling": is_big_castling
        }

    def get_piece_move_with_code(self, chess: Chess) -> CmdRequest:
        piece: Union[None, AbstractPiece] = None
        algebraic_notation: Dict = self.get_algebraic_notation()

        # castling
        if algebraic_notation["is_small_castling"] or algebraic_notation["is_big_castling"]:
            piece = chess.get_own_king()
            algebraic_notation["which_piece_position"] = piece.position.get_real_position()

        if algebraic_notation["is_small_castling"]:
            cell_id = algebraic_notation["which_piece_position"] + 2
        elif algebraic_notation["is_big_castling"]:
            cell_id = algebraic_notation["which_piece_position"] - 2
        # end castling
        else:
            cell_id = Position.get_real_position_by_x_y(
                int(algebraic_notation["destination_move_x_y"][1]),
                self.charset_column[algebraic_notation["destination_move_x_y"][0]]
            )

            # detect witch piece player want move
            pieces_list = []
            for own_piece in chess.get_own_pieces().values():
                if isinstance(own_piece, self.pieces_short[algebraic_notation["piece"]]):
                    all_moves = own_piece.get_real_moves(chess.board.get_all_pieces()).moves
                    all_attacks = own_piece.get_real_attack(chess.board.get_all_pieces_by_color()).attacks

                    if (
                            (not algebraic_notation["is_attack"] and cell_id in all_moves)
                            or (algebraic_notation["is_attack"] and cell_id in all_attacks)
                    ):
                        pieces_list.append(own_piece)

            if len(pieces_list) != 1:
                which_piece_position: str = algebraic_notation["which_piece_position"]
                row = None
                column = None

                if not which_piece_position:
                    raise InvalidMove("invalid input you can move multi piece")

                if len(which_piece_position) == 2:
                    row = int(which_piece_position[1])
                    column = self.charset_column[which_piece_position[0]]
                elif which_piece_position.isnumeric():
                    row = int(which_piece_position)
                else:
                    column = self.charset_column[which_piece_position]

                for piece_ in pieces_list:
                    if (row is not None) and piece_.position.x == row:
                        if (column is not None) and piece_.position.y != column:
                            continue
                        if piece is not None:
                            raise InvalidMove("invalid input you can move multi piece")
                        piece = piece_

                    elif (column is not None) and piece_.position.y == column:
                        if (row is not None) and piece_.position.x != row:
                            continue
                        if piece is not None:
                            raise InvalidMove("invalid input you can move multi piece")
                        piece = piece_
            else:
                piece = pieces_list[0]
            # end detect witch piece player want move

        return CmdRequest(
            status_code=0,
            message="move successfully",
            piece=piece,
            which_piece_position=algebraic_notation["which_piece_position"],
            destination_move_position=cell_id,
            is_attack=algebraic_notation["is_attack"],
            is_check=algebraic_notation["is_check"],
            is_double_check=algebraic_notation["is_double_check"],
            is_check_mate=algebraic_notation["is_check_mate"],
            is_small_castling=algebraic_notation["is_small_castling"],
            is_big_castling=algebraic_notation["is_big_castling"],
        )
