class IsKilledError(Exception):
    pass


class PieceIsKilled:
    def __init__(self, is_killed: bool):
        self.is_killed: bool = is_killed

    @property
    def is_killed(self) -> bool:
        return self._is_killed

    @is_killed.setter
    def is_killed(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise IsKilledError(f"you have set wrong is_killed. your is_killed is: {value}")
        self._is_killed = value

    def __str__(self):
        return self._is_killed
