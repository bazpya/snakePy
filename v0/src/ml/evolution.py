from src.ml.player import Player
from src.game.result import Result
from src.ml.generation import Generation, GenerationResult
from src.config import config
import time


class Evolution:

    def __init__(self, verbose: bool = False) -> None:
        self._has_ancestor_file = config.ml.evolution.has_ancestor_file
        self._gen_count = config.ml.evolution.generations
        self._fitness_trend = dict()
        self._last_gen_res = None
        self._verbose = verbose

    async def run(self) -> "EvolutionResult":
        self._verbose and print("Evolution began ...")
        res: GenerationResult = None
        time_start = time.time()
        for i in range(self._gen_count):
            has_ancestor_file = self._has_ancestor_file if i == 0 else False
            gen = Generation(
                id=i,
                previous_res=res,
                has_ancestor_file=has_ancestor_file,
                verbose=self._verbose,
            )
            res = await gen.run()
            self._last_gen_res = res
            self._fitness_trend[i] = res.max_fitness
        time_end = time.time()
        time_diff = time_end - time_start
        self._verbose and print("Evolution ended")

        return EvolutionResult(
            self._gen_count,
            self._fitness_trend,
            time_diff,
            [x.player for x in self._last_gen_res.fittest],
        )


class EvolutionResult(Result):
    def __init__(
        self,
        generations: int,
        fitness_trend: dict,
        time_taken: float,
        fittest: list[Player],
    ) -> None:
        self.generations = generations
        self.fitness_trend = fitness_trend
        self.time_taken = time_taken
        self.fittest = fittest
