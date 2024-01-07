class Counter:
    _value: int

    def __init__(self) -> None:
        self._value = 0

    def increment(self, *args, **kwargs) -> int:
        self._value += 1
        return self._value

    def read(self) -> int:
        return self._value
