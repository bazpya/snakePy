from src.game.global_refs import CauseOfDeath
from src.game.cell import Cell
from src.game.direction import Turn


class SnakeResult:
    def __init__(
        self,
        steps_taken: int,
        length: int,
        cause_of_death: CauseOfDeath,
    ) -> None:
        self.steps_taken = steps_taken
        self.length = length
        self.cause_of_death = cause_of_death


class GameResult:
    def __init__(
        self,
        row_count: int,
        col_count: int,
        snake_res: SnakeResult,
    ) -> None:
        self.row_count = row_count
        self.col_count = col_count
        self.steps_taken = snake_res.steps_taken
        self.length = snake_res.length
        self.cause_of_death = snake_res.cause_of_death


class PlayerResult:
    pass
