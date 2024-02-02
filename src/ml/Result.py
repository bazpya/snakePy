from src.game.Result import Result, GameResult


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


class GenerationResult(Result):
    def __init__(
        self,
        id: int,
        selection_count: int,
        results: list[PlayerResult],
    ) -> None:
        self.id = id
        sorted_res = sorted(results, key=lambda x: x.fitness, reverse=True)
        self.top_results = sorted_res[:selection_count]
        # self.top_ids = [r.id for r in sorted_res]
        self.max_fitness = sorted_res[0].fitness
        self.min_fitness = sorted_res[-1].fitness


# class EvolutionResult(Result):
#     pass
