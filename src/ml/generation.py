import asyncio
import math
from src.args import Args
from src.config import config
from src.game.result import Result
from src.ml.player import Player, PlayerResult
from src.game.drawer import Drawer


class Generation:
    def __init__(
        self,
        id: int,
        previous_res: "GenerationResult" = None,
        has_ancestor_file: bool = False,
        verbose: bool = False,
    ) -> None:
        self.use_ui = Args.use_ui
        self.population = config.ml.generation.population
        selection_ratio = config.ml.evolution.selection_ratio
        self.selection_count = math.floor(self.population * selection_ratio)
        if self.selection_count < 1:
            raise ValueError("No player survives the harsh selection ratio")
        self._id = id
        if previous_res is not None and has_ancestor_file:
            raise ValueError(
                "A generation with ancestor from file may not inherit result from previous generation"
            )
        self._previous_res = previous_res
        self._has_ancestor_file = has_ancestor_file

        self._players: list[Player] = []
        self._drawers: list[Drawer] = []
        self._coroutines = []
        self._player_results: list[PlayerResult] = []

        self._verbose = verbose

        self._populate()
        self._bind()
        self._make_coroutines()

    def _populate(self):
        parents = []
        if self._previous_res:
            parents = [x.player for x in self._previous_res.fittest]
        for i, parent in enumerate(parents):
            clone = parent.clone(i)
            self._players.append(clone)
        for i in range(len(parents), self.population):
            player = Player(id=i, verbose=self._verbose)
            self._players.append(player)

    def _bind(self):
        for player in self._players:
            player.events.died.subscribe(self._add_res)

    def _make_coroutines(self):
        for player in self._players:

            async def async_func():
                drawer = Drawer(player._game)
                self._drawers.append(drawer)
                await player.play_async()
                # drawer.getMouse()

            if self.use_ui:
                self._coroutines.append(async_func())
            else:
                self._coroutines.append(player.play_awaitable_sync())

    def _add_res(self, res: PlayerResult):
        self._player_results.append(res)

    async def run(self):
        self._verbose and print(f"Generation {self._id} running")
        await asyncio.gather(*self._coroutines)
        return GenerationResult(
            self._id,
            self.selection_count,
            self._player_results,
        )


class GenerationResult(Result):
    def __init__(
        self,
        id: int,
        selection_count: int,
        results: list[PlayerResult],
    ) -> None:
        sorted_res = sorted(results, key=lambda x: x.fitness, reverse=True)
        self.fittest = sorted_res[:selection_count]
        self.id = id
        self.max_fitness = sorted_res[0].fitness
        self.min_fitness = sorted_res[-1].fitness
