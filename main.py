import asyncio
import time
from src.ml.player import Player
from src.ml.Result import PlayerResult
from src.ml.player_fake import PlayerFake
from src.config import Config
from src.game.drawer import Drawer
from src.game.game import Game

use_ui = Config.get("game.use_ui")
row_count = Config.get("game.row_count")
col_count = Config.get("game.col_count")
cell_size = Config.get("game.cell_size")
food_count = Config.get("game.food_count")
interval = Config.get("game.interval")

use_fake_player = Config.get("ml.use_fake_player")
player_count = Config.get("ml.player_count")


result: list[PlayerResult] = []


def collect_res(res: PlayerResult):
    result.append(res)


def print_res():
    for res in result:
        print(res.serialise())


coroutines = []
drawers: list[Drawer] = []


def make_coroutine(has_ui: bool, id: int):
    game = Game(row_count, col_count, food_count)
    player = PlayerFake(game, i) if use_fake_player else Player(game, i, None)
    player.events.died.subscribe(collect_res)

    async def async_func():
        drawer = Drawer(cell_size)
        drawer.bind(game)
        drawers.append(drawer)
        await player.play_async(interval)
        drawer.getMouse()

    async def sync_func():
        player.play_sync()

    if has_ui:
        return async_func()
    else:
        return sync_func()


for i in range(0, player_count):
    if use_ui:
        coroutine = make_coroutine(True, i)
    else:
        coroutine = make_coroutine(False, i)
    coroutines.append(coroutine)


async def func():
    batch = asyncio.gather(*coroutines)
    await batch


time_start = time.time()
asyncio.run(func())
time_end = time.time()

time_diff = time_end - time_start

print_res()
print(f"Time taken: {time_diff} seconds")
