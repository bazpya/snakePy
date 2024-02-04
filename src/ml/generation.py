import asyncio
from src.game.result import Result
from src.ml.generation_spec import GenerationSpec
from src.ml.eye import Eye
from src.ml.eye_fake import EyeFake
from src.ml.player import Player, PlayerResult
from src.ml.player_fake import PlayerFake
from src.game.drawer import Drawer
from src.game.game import Game


class Generation:
    def __init__(
        self, id: int, specs: GenerationSpec, parents: list[Player] = []
    ) -> None:
        self._id = id
        self._specs = specs
        self._players: list[Player] = []
        self._drawers: list[Drawer] = []
        self._coroutines = []
        self._player_results: list[PlayerResult] = []

        self._populate()
        self._bind()
        self._make_coroutines()

        for i in range(self._specs.population):
            coroutine = self.make_coroutine(i)
            self._coroutines.append(coroutine)

    def _populate(self):
        pass

    def _bind(self):
        pass

    def _make_coroutines(self):
        pass

    def make_coroutine(self, id: int):
        game = Game(
            self._specs.row_count,
            self._specs.col_count,
            self._specs.max_steps,
        )
        if self._specs.fake_player:
            fake_eye = EyeFake(self._specs.view)
            player = PlayerFake(id, game, fake_eye)
        else:
            eye = Eye(self._specs.view)
            player = Player(id, game, eye)
        player.events.died.subscribe(self.add_res)

        async def async_func():
            drawer = Drawer(self._specs.cell_size)
            drawer.bind(game)
            self._drawers.append(drawer)
            await player.play_async(self._specs.interval)
            # drawer.getMouse()

        if self._specs.use_ui:
            return async_func()
        else:
            return player.play_awaitable_sync()

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
