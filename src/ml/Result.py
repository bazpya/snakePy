from enum import Enum
import json
from src.game.Result import GameResult


class PlayerResult:
    def __init__(
        self,
        id: int,
        game_res: GameResult,
    ) -> None:
        self.id = id
        self.row_count = game_res.row_count
        self.col_count = game_res.col_count
        self.steps_taken = game_res.steps_taken
        self.length = game_res.length
        self.cause_of_death = game_res.cause_of_death

    def serialise(self):
        return json.dumps(
            self.__dict__,
            default=self.serialiser_func,
            indent=2,
        )

    def serialiser_func(self, x):
        if isinstance(x, Enum):
            return x.name
        else:
            return x


class GenerationResult:
    pass


class EvolutionResult:
    pass
