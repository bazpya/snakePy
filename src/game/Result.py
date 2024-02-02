from enum import Enum
import json
from src.game.global_refs import CauseOfDeath


class Result:
    def serialise(self) -> str:
        return json.dumps(
            self.__dict__,
            default=self.serialiser_func,
            indent=2,
        )

    def serialiser_func(self, x) -> object:
        if isinstance(x, Enum):
            return x.name
        elif isinstance(x, Result):
            return x.__dict__
        else:
            return x


class SnakeResult(Result):
    def __init__(
        self,
        steps_taken: int,
        length: int,
        cause_of_death: CauseOfDeath,
        cells_visited: int,
    ) -> None:
        self.steps_taken = steps_taken
        self.length = length
        self.cause_of_death = cause_of_death
        self.cells_visited = cells_visited


class GameResult(SnakeResult):
    def __init__(
        self,
        row_count: int,
        col_count: int,
        snake_res: SnakeResult,
    ) -> None:
        self.row_count = row_count
        self.col_count = col_count
        self.snake = snake_res
