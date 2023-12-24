from enum import Enum


class CellType(Enum):
    blank = 1
    wall = 2
    worm = 3
    food = 4


class Direction(Enum):
    up = 1
    right = 2
    down = 3
    left = 4
