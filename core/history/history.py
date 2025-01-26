from typing import List, Union
from .history_turn import HistoryTurn
from utils.log import core_logger


class History:
    def __init__(self):
        self._history: List[HistoryTurn] = []
        core_logger.info("History initialised")

    def append(self, history: HistoryTurn) -> None:
        self._history.append(history)

    def get(self) -> Union[HistoryTurn, None]:
        try:
            return self._history[-1]
        except IndexError:
            return None

    def __iter__(self):
        self._index = 0
        return self

    def __next__(self):
        if self._index < len(self._history):
            result = self._history[self._index]
            self._index += 1
            return result
        else:
            raise StopIteration

    def __len__(self):
        return len(self._history)

    def __getitem__(self, index: int) -> HistoryTurn:
        if index < 0 or index >= len(self._history):
            raise IndexError("Index out of range")

        return self._history[index]

    def __setitem__(self, index: int, value: HistoryTurn) -> None:
        if index < 0 or index >= len(self._history):
            raise IndexError("Index out of range")

        if not isinstance(value, HistoryTurn):
            raise TypeError("Value must be of type HistoryTurn")

        self._history[index] = value

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'

    def __str__(self) -> str:
        return f'{len(self._history)}'
