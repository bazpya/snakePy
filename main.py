import asyncio
from source.drawer import Drawer
from source.game import Game

game = Game(24)
worm = game.add_worm()
game._drop_food()
drawer = Drawer()


def update():
    drawer.draw(game._cells)


game.event_hub.stepped.subscribe(update)
task = worm.run(0.1, 7)
res = asyncio.get_event_loop().run_until_complete(task)

drawer.getMouse()
