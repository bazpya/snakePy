from enum import Enum


class Turn(Enum):
    left = -1
    ahead = 0
    right = 1


class Direction(Enum):
    up = 0  # todo: add diagonals
    right = 1
    down = 2
    left = 3

    def is_aligned(self, dir: "Direction") -> bool:
        return self.value % 2 == dir.value % 2

    def is_perpendicular(self, dir: "Direction") -> bool:
        return not self.is_aligned(dir)

    def get_opposite(self) -> "Direction":
        value = (self.value + 2) % len(Direction)
        return Direction(value)

    def turn(self, turn: Turn) -> "Direction":
        val = (self.value + turn.value) % len(Direction)
        return Direction(val)
