from src.game.Result import GameResult


class PlayerResult(GameResult):
    def __init__(
        self,
        id: int,
        fitness: float,
        game_res: GameResult,
    ) -> None:
        self.id = id
        self.fitness = fitness
        self.game = game_res


class GenerationResult:
    pass


class EvolutionResult:
    pass
