import asyncio
from source.drawer import Drawer
from source.game import Game

game = Game(64, 3)
worm = game.add_worm()
game._drop_food()
drawer = Drawer()
drawer.draw(game.get_cells())


def update(*args, **kwargs):
    drawer.draw(game._step_diff_cells)
    game._purge_diff()


game.event_hub.stepped.subscribe(update)
task = worm.run(0.1, 27)
res = asyncio.get_event_loop().run_until_complete(task)

drawer.getMouse()
