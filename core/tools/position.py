from typing import Union, Tuple


class PositionError(ValueError):
    pass


class Position:
    def __init__(self, pos_x: int, pos_y: Union[int, None] = None) -> None:
        if pos_y is None:
            if not (64 >= pos_x >= 1):
                raise PositionError(
                    f"the position is not valid position,"
                    f" position must between and equal 1 and 64 "
                    f"your pos: {pos_x}"
                )
        else:
            if not (8 >= pos_x >= 1) or not (8 >= pos_y >= 1):
                raise PositionError(f"the position is not valid position your pos_x: {pos_x} and pos_y: {pos_y}")

        if pos_y is not None:
            self.x = pos_x
            self.y = pos_y
        else:
            self.x, self.y = self.get_x_y_from_position(pos_x)

        self.last_position: Union[None, Tuple[int, int]] = None

    def get_x_y(self) -> Tuple[int, int]:
        return self.x, self.y

    def get_real_position(self) -> int:
        return self.get_real_position_by_x_y(self.x, self.y)

    def get_last_position(self) -> Tuple[int, int]:
        if self.last_position is None:
            raise RuntimeError("cant return to None position")
        return self.last_position

    def get_last_real_position(self):
        return self.get_real_position_by_x_y(*self.get_last_position())

    def return_to_last_position(self) -> None:
        self.x, self.y = self.get_last_position()
        self.last_position = None

    def set_position(self, pos_x: Union[int, str], pos_y: Union[int, None] = None) -> None:
        self.last_position = self.get_x_y()
        if pos_y is None:
            if isinstance(pos_x, str) and "X" in pos_x:
                self.x, self.y = [int(pos) for pos in pos_x.split("X")]
            else:
                self.x, self.y = self.get_x_y_from_position(pos_x)
        else:
            self.x, self.y = pos_x, pos_y

    @staticmethod
    def get_x_y_from_position(position: int) -> Tuple[int, int]:
        return (position - 1) // 8 + 1, (position - 1) % 8 + 1

    @staticmethod
    def get_real_position_by_x_y(pos_x: int, pos_y: int) -> int:
        return (pos_x - 1) * 8 + pos_y

    @staticmethod
    def get_pos_or_false_by_x_y(pos_x: int, pos_y: int) -> Union[int, bool]:
        if (1 <= pos_x <= 8) and (1 <= pos_y <= 8):
            return Position.get_real_position_by_x_y(pos_x, pos_y)
        else:
            return False

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(pos_x={self.x}, pos_y={self.y})"

    def __str__(self) -> str:
        return f"{self.x}X{self.y}"
