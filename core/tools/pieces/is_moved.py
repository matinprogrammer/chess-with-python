class IsMovedError(Exception):
    pass


class PieceIsMoved:
    def __init__(self, is_moved: bool):
        self.is_moved: bool = is_moved

    @property
    def is_moved(self) -> bool:
        return self.is_moved

    @is_moved.setter
    def is_moved(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise IsMovedError(f"you have set wrong is_moved. your is_moved is: {value}")
        self.is_moved = value

    def __str__(self):
        return self.is_moved
