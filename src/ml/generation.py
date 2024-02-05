import asyncio
from src.game.result import Result
from src.ml.generation_spec import GenerationSpec
from src.ml.eye import Eye
from src.ml.player import Player, PlayerResult
from src.game.drawer import Drawer
from src.game.game import Game


class Generation:
    def __init__(
        self,
        id: int,
        specs: GenerationSpec,
        previous_res: "GenerationResult" = None,
    ) -> None:
        if specs.selection_count < 1:
            raise ValueError("No player survives the harsh selection ratio")

        self._id = id
        self._specs = specs
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
            game = Game(
                self._specs.row_count, self._specs.col_count, self._specs.max_steps
            )
            eye = Eye(self._specs.view)
            clone = parent.clone(i, game, eye)
            self._players.append(clone)
        for i in range(len(parents), self._specs.population):
            game = Game(
                self._specs.row_count, self._specs.col_count, self._specs.max_steps
            )
            eye = Eye(self._specs.view)
            player = Player(i, game, eye)
            self._players.append(player)

    def _bind(self):
        for player in self._players:
            player.events.died.subscribe(self.add_res)

    def _make_coroutines(self):
        for player in self._players:

            async def async_func():
                drawer = Drawer(self._specs.cell_size)
                drawer.bind(player._game)
                self._drawers.append(drawer)
                await player.play_async(self._specs.interval)
                # drawer.getMouse()

            if self._specs.use_ui:
                self._coroutines.append(async_func())
            else:
                self._coroutines.append(player.play_awaitable_sync())

    def add_res(self, res: PlayerResult):
        self._player_results.append(res)

    async def run(self):
        await asyncio.gather(*self._coroutines)
        return GenerationResult(
            self._id,
            self._specs.selection_count,
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
