import asyncio
from src.ml.view import View
from src.ml.eye import Eye
from src.ml.eye_fake import EyeFake
from src.ml.player import Player
from src.ml.player_fake import PlayerFake
from src.game.drawer import Drawer
from src.game.game import Game
from src.ml.Result import PlayerResult


class GenerationParam:
    def __init__(
        self,
        population: int,
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
        self.row_count = row_count
        self.col_count = col_count
        self.max_steps = max_steps
        self.fake_player = fake_player
        self.view = view
        self.use_ui = use_ui
        self.cell_size = cell_size
        self.interval = interval


class Generation:

    def __init__(self, param: GenerationParam) -> None:
        self._params = param
        self._player_res: list[PlayerResult] = []
        self._coroutines = []
        self._drawers: list[Drawer] = []
        for i in range(self._params.population):
            coroutine = self.make_coroutine(i)
            self._coroutines.append(coroutine)
        hasan = 5

    def make_coroutine(self, id: int):
        game = Game(
            self._params.row_count,
            self._params.col_count,
            self._params.max_steps,
        )
        if self._params.fake_player:
            fake_eye = EyeFake(self._params.view)
            player = PlayerFake(id, game, fake_eye)
        else:
            eye = Eye(self._params.view)
            player = Player(id, game, eye)
        player.events.died.subscribe(self.add_res)

        async def sync_func():
            player.play_sync()

        async def async_func():
            drawer = Drawer(self._params.cell_size)
            drawer.bind(game)
            self._drawers.append(drawer)
            await player.play_async(self._params.interval)
            # drawer.getMouse()

        if self._params.use_ui:
            return async_func()
        else:
            return sync_func()

    def add_res(self, res: PlayerResult):
        self._player_res.append(res)

    async def run(self):
        await asyncio.gather(*self._coroutines)
        return self._player_res
