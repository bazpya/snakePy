from src.game.cell import Cell
from src.game.direction import Turn


class SnakeResult:
    def __init__(self, steps_taken: int, length: int) -> None:
        self.steps_taken = steps_taken
        self.length = length


class GameResult:
    def __init__(
        self,
        row_count: int,
        col_count: int,
        foods: list[Cell],
        turns: list[Turn],
        snake_res: SnakeResult,
    ) -> None:
        self.row_count = row_count
        self.col_count = col_count
        self.steps_taken = snake_res.steps_taken
        self.length = snake_res.length
        self.foods = foods
        self.turns = turns


class PlayerResult:
    pass
