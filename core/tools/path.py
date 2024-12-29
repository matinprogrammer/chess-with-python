class Path:
    def __init__(self, path: str) -> None:
        self._path = path

    @property
    def path(self) -> str:
        return self._path

    @path.setter
    def path(self, value: str) -> None:
        if not isinstance(value, str):
            raise ValueError(f"Path must be a string")
        self._path = value

    def __truediv__(self, other: str) -> str:
        if not isinstance(other, str):
            raise ValueError(f"in divide assignment must be string")
        return self.path + other

    def __str__(self) -> str:
        return self.path
