from enum import Enum


class CellType(Enum):
    blank = 1
    wall = 2
    snake = 3
    food = 4


class Direction(Enum):
    up = 0
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
