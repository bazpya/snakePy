# Test doubles shared by tests in several packages
from snake.core import Cell


class FixedFoodPlacer:
    # Always places food on the same cell
    def __init__(self, cell: Cell) -> None:
        self._cell = cell

    def place_food(self, free) -> Cell:
        return self._cell
