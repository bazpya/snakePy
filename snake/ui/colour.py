from enum import StrEnum


class Colour(StrEnum):
    # What each kind of cell looks like; values are tkinter colour names
    empty = "black"
    body = "green"
    head = "lime"
    food = "yellow"
