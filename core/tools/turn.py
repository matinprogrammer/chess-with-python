from utils.log import core_logger


class TurnError(Exception):
    pass


class Turn:
    def __init__(self, turn_number: int):
        self.turn_number: int = turn_number

        # log
        core_logger.debug(f"Turn {self.turn_number} initialised")

    @property
    def turn_number(self) -> str:
        return self._turn_number

    @turn_number.setter
    def turn_number(self, value: str) -> None:
        if value < 1:
            raise TurnError("you can't assign less than 1")
        self._turn_number = value

    @property
    def turn_str(self) -> str:
        return "white" if self._turn_number % 2 == 1 else "black"

    def increase_turn(self) -> None:
        self._turn_number += 1

    def __str__(self) -> str:
        return self.turn_str
