import asyncio
from src.ml.view import View
from src.ml.eye import Eye
from src.ml.eye_fake import EyeFake
from src.ml.player import Player
from src.ml.player_fake import PlayerFake
from src.game.drawer import Drawer
from src.game.game import Game
from src.ml.Result import PlayerResult, GenerationResult


class GenerationSpecs:
    def __init__(
        self,
        population: int,
        selection_count: int,
        row_count: int,
        col_count: int,
        max_steps: int,
        fake_player: bool,
        view: View,
        use_ui: bool,
        cell_size: int,
        interval: float,
    ) -> None:
        self.population = population
        self.selection_count = selection_count
        self.row_count = row_count
        self.col_count = col_count
        self.max_steps = max_steps
        self.fake_player = fake_player
        self.view = view
        self.use_ui = use_ui
        self.cell_size = cell_size
        self.interval = interval


class Generation:

    def __init__(self, id: int, specs: GenerationSpecs) -> None:
        self._id = id
        self._specs = specs
        self._coroutines = []
        self._drawers: list[Drawer] = []
        for i in range(self._specs.population):
            coroutine = self.make_coroutine(i)
            self._coroutines.append(coroutine)
        self._player_results: list[PlayerResult] = []

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
