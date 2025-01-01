class PieceIdError(Exception):
    pass


class PieceId:
    id_counter = 1

    def __init__(self):
        self.piece_id = PieceId.id_counter
        PieceId.id_counter += 1

    @property
    def piece_id(self):
        return self.piece_id

    @piece_id.setter
    def piece_id(self, value: int):
        raise PieceIdError("you can't assign a piece_id")
