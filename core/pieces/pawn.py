from .abstract_piece import AbstractPiece
from .piece_request import PieceRequest
from typing import List, Dict
from ..tools import Position
from ..history import History
from abc import ABC
import itertools


class Pawn(AbstractPiece, ABC):
    def __init__(self, pawn_id, *args) -> None:
        super().__init__(*args)
        self.picture_path /= "pawn.png"
        self.id = pawn_id


class BPawn(Pawn):
    def get_all_moves(self) -> List[List[int]]:
        moves = [[]]
        if pos := Position.get_pos_or_false_by_x_y(self.position.x - 1, self.position.y):
            moves[0].append(pos)

        if not self.is_move:
            if pos := Position.get_pos_or_false_by_x_y(self.position.x - 2, self.position.y):
                moves[0].append(pos)

        return moves

    # override for add enpassant
    def get_real_attack(self, pieces_color: Dict[str, Dict[int, AbstractPiece]],
                        history: History = None) -> PieceRequest:
        attacks: List[int] = []
        pos_x, pos_y = self.position.get_x_y()

        if pos := self.position.get_pos_or_false_by_x_y(pos_x - 1, pos_y + 1):
            if pos in pieces_color[self.opponent_color].keys():
                attacks.append(pos)

        if pos := self.position.get_pos_or_false_by_x_y(pos_x - 1, pos_y - 1):
            if pos in pieces_color[self.opponent_color].keys():
                attacks.append(pos)

        # enpassant
        is_enpassant = False
        attack_to_position = attacks.copy()
        enpassant_attacks = []
        if history is not None:
            if (history_turn := history.get()) is not None:
                if (
                        isinstance(history_turn.piece, WPawn) and
                        (history_turn.from_position.x + 2 == history_turn.to_position.x)
                ):
                    if ((pos := self.position.get_pos_or_false_by_x_y(pos_x, pos_y + 1))
                            == history_turn.to_position.get_real_position()):
                        enpassant_attacks.append(pos - 8)
                        attack_to_position.append(pos)
                        is_enpassant = True

                    if ((pos := self.position.get_pos_or_false_by_x_y(pos_x, pos_y - 1))
                            == history_turn.to_position.get_real_position()):
                        enpassant_attacks.append(pos - 8)
                        attack_to_position.append(pos)
                        is_enpassant = True
        # end enpassant

        return PieceRequest(
            attacks=attacks + enpassant_attacks,
            oppoonent_pieces=[
                pieces_color[self.opponent_color].get(piece_position) for piece_position in attack_to_position
            ],
            is_enpassant=is_enpassant,
            attack_from_position=list(
                itertools.repeat(self.position.get_real_position(), len(attacks) + len(enpassant_attacks))
            ),
            attack_to_position=attack_to_position
        )


class WPawn(Pawn):
    def get_all_moves(self) -> List[List[int]]:
        moves = [[]]
        if pos := Position.get_pos_or_false_by_x_y(self.position.x + 1, self.position.y):
            moves[0].append(pos)

        if not self.is_move:
            if pos := Position.get_pos_or_false_by_x_y(self.position.x + 2, self.position.y):
                moves[0].append(pos)

        return moves

    # override for add enpassant
    def get_real_attack(self, pieces_color: Dict[str, Dict[int, AbstractPiece]],
                        history: History = None) -> PieceRequest:
        attacks: List[int] = []
        pos_x, pos_y = self.position.get_x_y()

        if pos := self.position.get_pos_or_false_by_x_y(pos_x + 1, pos_y + 1):
            if pos in pieces_color[self.opponent_color].keys():
                attacks.append(pos)

        if pos := self.position.get_pos_or_false_by_x_y(pos_x + 1, pos_y - 1):
            if pos in pieces_color[self.opponent_color].keys():
                attacks.append(pos)

        # enpassant
        is_enpassant = False
        attack_to_position = attacks.copy()
        enpassant_attacks = []
        if history is not None:
            # enpassant
            if (history_turn := history.get()) is not None:
                if (
                        isinstance(history_turn.piece, BPawn) and
                        (history_turn.from_position.x - 2 == history_turn.to_position.x)
                ):
                    if ((pos := self.position.get_pos_or_false_by_x_y(pos_x, pos_y + 1))
                            == history_turn.to_position.get_real_position()):
                        enpassant_attacks.append(pos + 8)
                        attack_to_position.append(pos)
                        is_enpassant = True

                    if ((pos := self.position.get_pos_or_false_by_x_y(pos_x, pos_y - 1))
                            == history_turn.to_position.get_real_position()):
                        enpassant_attacks.append(pos + 8)
                        attack_to_position.append(pos)
                        is_enpassant = True
        # end enpassant

        return PieceRequest(
            attacks=attacks + enpassant_attacks,
            oppoonent_pieces=[
                pieces_color[self.opponent_color].get(piece_position) for piece_position in attack_to_position
            ],
            is_enpassant=is_enpassant,
            attack_from_position=list(
                itertools.repeat(self.position.get_real_position(), len(attacks) + len(enpassant_attacks))
            ),
            attack_to_position=attack_to_position
        )
