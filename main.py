import asyncio
from source.drawer import Drawer
from source.game import Game

game = Game(3, 64)
snake = game.add_snake()
game._add_food()
drawer = Drawer()
drawer.draw(game.get_cells())


def redraw(*args, **kwargs):
    drawer.draw(*args)


game.event_hub.ready_to_draw.subscribe(redraw)
task = snake.run(0.1, 27)
res = asyncio.get_event_loop().run_until_complete(task)

drawer.getMouse()
