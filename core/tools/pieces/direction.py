from utils.log import core_logger


class DirectionError(Exception):
    pass


class PieceDirection:
    def __init__(self, direction: str):
        self.direction: str = direction

        # log
        core_logger.debug(f"PieceDirection {self.direction} initialised")

    @property
    def direction(self) -> str:
        return self._direction

    @direction.setter
    def direction(self, value: str) -> None:
        if value is not None:
            lover_value = value.lower()
            if lover_value not in ["left", "right"]:
                raise DirectionError(f"you have set wrong direction. your direction is: {value}")
            self._direction = lover_value
        else:
            self._direction = None

    def __str__(self):
        return self._direction
