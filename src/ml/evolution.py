from src.game.result import Result
from src.ml.generation import Generation
from src.config import config
import time


class Evolution:

    def __init__(self, generation_count: int = 0) -> None:
        if generation_count:
            self._gen_count = generation_count
        else:
            self._gen_count = config.ml.evolution.generations
        self._fitness_trend = dict()

    async def run(self) -> None:
        res = None
        time_start = time.time()
        for i in range(self._gen_count):
            gen = Generation(i, res)
            res = await gen.run()
            self._fitness_trend[i] = res.max_fitness
        time_end = time.time()
        time_diff = time_end - time_start

        return EvolutionResult(
            self._gen_count,
            self._fitness_trend,
            time_diff,
        )


class EvolutionResult(Result):
    def __init__(
        self,
        generations: int,
        fitness_trend: dict,
        time_taken: float,
    ) -> None:
        self.generations = generations
        self.fitness_trend = fitness_trend
        self.time_taken = time_taken
