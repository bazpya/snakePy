from src.game.Result import GameResult


class PlayerResult(GameResult):
    def __init__(
        self,
        id: int,
        game_res: GameResult,
    ) -> None:
        self.id = id
        self.game = game_res


class GenerationResult:
    pass


class EvolutionResult:
    pass
