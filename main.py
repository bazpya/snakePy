import sys
import asyncio
from source.drawer import Drawer
from source.game import Game

args = sys.argv
switch = args[1] if len(args) > 1 else None

game = Game(3, 64)
snake = game.add_snake()
game._add_food()
drawer = Drawer()
drawer.draw(game.get_cells())


def redraw(*args, **kwargs):
    drawer.draw(*args)


if switch == "headless":
    drawer.getMouse()
    snake.run_sync()
    drawer.draw(game.get_cells())
    drawer.getMouse()
else:
    game.event_hub.ready_to_draw.subscribe(redraw)
    task = snake.run_async(0.03)
    res = asyncio.get_event_loop().run_until_complete(task)

    drawer.getMouse()
