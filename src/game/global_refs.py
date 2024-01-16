from enum import Enum


class CellType(Enum):
    blank = 0
    wall = 1
    snake = 2
    food = 3


class Anonym:  # todo: use this to bundle params of Brain init
    def __init__(self, **attributes):
        self.__dict__.update(attributes)
