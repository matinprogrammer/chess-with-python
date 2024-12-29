class DirectionError(Exception):
    pass


class PieceDirection:
    def __init__(self, direction: str):
        self.direction: str = direction

    @property
    def direction(self) -> str:
        return self.direction

    @direction.setter
    def direction(self, value: str) -> None:
        lover_value = value.lower()
        if lover_value not in ["left", "right"]:
            raise DirectionError(f"you have set wrong direction. your direction is: {value}")
        self.direction = lover_value

    def __str__(self):
        return self.direction
