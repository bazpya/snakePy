from enum import Enum


class CellType(Enum):
    blank = 0
    wall = 1
    snake = 2
    food = 3


class CauseOfDeath(Enum):
    steps_taken = 0
    snake = 1
    wall = 2
