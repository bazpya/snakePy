import sys
import asyncio
from src.ml.player_fake import PlayerFake
from src.config import Config
from src.game.drawer import Drawer
from src.game.game import Game

args = sys.argv
switch = args[1] if len(args) > 1 else None
is_headless = switch in ["-h", "headless"]
row_count = Config.get("game.row_count")
col_count = Config.get("game.col_count")
cell_size = Config.get("game.cell_size")
food_count = Config.get("game.food_count")
interval = Config.get("game.interval")

player_count: int = 1

for i in range(0, player_count):
    game = Game(row_count, col_count)
    player = PlayerFake(game)
    game._add_food(food_count)

    if is_headless:
        player.play_sync()
        print("done")
    else:
        drawer = Drawer(cell_size, row_count, col_count)
        drawer.draw(game.get_cells())
        game._events.ready_to_draw.subscribe(drawer.draw)
        task = player.play_async(interval)
        res = asyncio.get_event_loop().run_until_complete(task)
        drawer.getMouse()
