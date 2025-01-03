from utils.log import core_logger


class IsMovedError(Exception):
    pass


class PieceIsMoved:
    def __init__(self, is_moved: bool):
        self.is_moved: bool = is_moved

        # log
        core_logger.debug(f"PieceIsMoved: {self.is_moved} initialised")

    def set(self, value: bool) -> None:
        self.is_moved = value

    def get(self):
        return self.is_moved

    @property
    def is_moved(self) -> bool:
        return self._is_moved

    @is_moved.setter
    def is_moved(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise IsMovedError(f"you have set wrong is_moved. your is_moved is: {value}")
        self._is_moved = value

    def __str__(self):
        return self._is_moved
