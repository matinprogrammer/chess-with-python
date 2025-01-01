class PieceIdError(Exception):
    pass


class PieceId:
    id_counter = 1

    def __init__(self):
        self.piece_id = PieceId.id_counter
        PieceId.id_counter += 1

    @property
    def piece_id(self):
        return self._piece_id

    @piece_id.setter
    def piece_id(self, value: int):
        if value < 1:
            raise PieceIdError("you can't assign less than 1")
        self._piece_id = value
