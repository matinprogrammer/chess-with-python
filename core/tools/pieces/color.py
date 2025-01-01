class ColorError(Exception):
    pass


class PieceColor:
    def __init__(self, color: str):
        self.color: str = color

    @property
    def color(self) -> str:
        return self.color

    @color.setter
    def color(self, value: str) -> None:
        lover_value = value.lower()
        if lover_value not in ["white", "black"]:
            raise ColorError(f"you have set wrong color. your color is: {value}")
        self.color = lover_value

    @property
    def opponent_color(self) -> str:
        return "white" if self.color == "black" else "black"

    def __str__(self):
        return self.color
