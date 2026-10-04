from enum import Enum


class Turn(Enum):
    # Values are rotation offsets: Direction adds them
    # to turn clockwise (+) or anticlockwise (-)
    left = -1
    ahead = 0
    right = 1
