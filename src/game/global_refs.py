from enum import Enum


class CellType(Enum):
    blank = 0
    wall = 1
    snake = 2
    food = 3
