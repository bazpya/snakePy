from enum import Enum, auto


class EndCause(Enum):
    crashed = auto()  # into a wall or the body
    won = auto()  # filled the grid: no free cell left
    starved = auto()  # too long without food
