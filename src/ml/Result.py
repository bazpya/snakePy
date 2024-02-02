from src.game import Result
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


# class GenerationResult(Result):
#     max_fitness: float = 0
#     min_fitness: float = 0
#     top_players: list = []

#     def __init__(
#         self,
#         id: int,
#     ) -> None:
#         self.id = id


# class EvolutionResult(Result):
#     pass
