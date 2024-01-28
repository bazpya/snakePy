import sys
import asyncio
from src.game.Result import GameResult
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


def print_res(res: GameResult):
    print(res.serialise())


for i in range(0, player_count):
    game = Game(row_count, col_count, food_count)
    player = PlayerFake(game)
    game.events.died.subscribe(print_res)

    if is_headless:
        player.play_sync()
    else:
        drawer = Drawer(cell_size)
        drawer.bind(game)
        task = player.play_async(interval)
        res = asyncio.get_event_loop().run_until_complete(task)
        drawer.getMouse()

# def func(*args, **kwargs):
#     thread_number = i
#     print(f"thread {thread_number} start")
#     sleep(1)
#     print(f"thread {thread_number} end")


# if __name__ == "__main__":
#     count = 20
#     threads = []
#     for i in range(count):
#         thread = Thread(target=func, args=[])
#         threads.append(thread)
#         thread.start()

#     for i in range(count):
#         thread: Thread = threads[i]
#         thread.join(4.0)

#     print("finished")
