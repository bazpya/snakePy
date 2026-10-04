from typing import Protocol, Sequence
from snake.core.cell import Cell


class FoodPlacerConcept(Protocol):
    # What World needs from a food placer; FoodPlacer implements it
    def place_food(self, free: Sequence[Cell]) -> Cell: ...
