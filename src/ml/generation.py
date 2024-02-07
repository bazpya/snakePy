import asyncio
import math
from src.config import config
from src.game.result import Result
from src.ml.player import Player, PlayerResult
from src.game.drawer import Drawer


class Generation:
    def __init__(
        self,
        id: int,
        previous_res: "GenerationResult" = None,
    ) -> None:
        self.use_ui = config.game.use_ui
        self.population = config.ml.generation.population
        selection_ratio = config.ml.evolution.selection_ratio
        self.selection_count = math.floor(self.population * selection_ratio)
        if self.selection_count < 1:
            raise ValueError("No player survives the harsh selection ratio")

        self._id = id
        self._previous_res = previous_res

        self._players: list[Player] = []
        self._drawers: list[Drawer] = []
        self._coroutines = []
        self._player_results: list[PlayerResult] = []

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
            player = Player(i)
            self._players.append(player)

    def _bind(self):
        for player in self._players:
            player.events.died.subscribe(self.add_res)

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

    def add_res(self, res: PlayerResult):
        self._player_results.append(res)

    async def run(self):
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
        self.id = id
        sorted_res = sorted(results, key=lambda x: x.fitness, reverse=True)
        self.fittest = sorted_res[:selection_count]
        self.max_fitness = sorted_res[0].fitness
        self.min_fitness = sorted_res[-1].fitness
