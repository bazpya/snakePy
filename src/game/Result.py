from src.game.cell import Cell
from src.game.direction import Turn


class SnakeResult:
    def __init__(self, steps_taken: int, length: int) -> None:
        self.steps_taken = steps_taken
        self.length = length


class GameResult:
    def __init__(
        self,
        width: int,
        height: int,
        steps_taken: int,
        length: int,
        foods: list[Cell],
        turns: list[Turn],
    ) -> None:
        self.width = width
        self.height = height
        self.steps_taken = steps_taken
        self.length = length
        self.foods = foods
        self.turns = turns


class PlayerResult:
    pass
