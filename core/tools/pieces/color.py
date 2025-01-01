class ColorError(Exception):
    pass


class OpponentColorError(Exception):
    pass


class PieceColor:
    def __init__(self, color: str):
        self.color: str = color

    @property
    def color(self) -> str:
        return self._color

    @color.setter
    def color(self, value: str) -> None:
        lover_value = value.lower()
        if lover_value not in ["white", "black"]:
            raise ColorError(f"you have set wrong color. your color is: {value}")
        self._color = lover_value

    @property
    def opponent(self) -> str:
        return "white" if self._color == "black" else "black"

    @opponent.setter
    def opponent(self, value: str) -> None:
        raise OpponentColorError("you cant assignment value to opponent_color")

    def __str__(self):
        return self._color
