from utils.log import core_logger


class IsKilledError(Exception):
    pass


class PieceIsKilled:
    def __init__(self, is_killed: bool):
        self.is_killed: bool = is_killed

        # log
        core_logger.debug(f"PieceIsKilled {self.is_killed} initialised")

    def set(self, value: bool) -> None:
        self.is_killed = value

    def get(self) -> bool:
        return self.is_killed

    @property
    def is_killed(self) -> bool:
        return self._is_killed

    @is_killed.setter
    def is_killed(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise IsKilledError(f"you have set wrong is_killed. your is_killed is: {value}")
        self._is_killed = value

    def __str__(self) -> str:
        return str(self._is_killed)
