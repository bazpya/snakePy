import random
from typing import Sequence
from snake.core.cell import Cell
from snake.core.food_placer_concept import FoodPlacerConcept


class FoodPlacer(FoodPlacerConcept):
    # Picks where food goes; the World decides which cells are free

    def __init__(self, rng: random.Random | None = None) -> None:
        self._rng = rng or random.Random()

    def place_food(self, free: Sequence[Cell]) -> Cell:
        return self._rng.choice(free)
