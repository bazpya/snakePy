from source.drawer import Drawer
from source.game import Game

game = Game(8)
game.add_worm()
game._drop_food()
drawer = Drawer()
drawer.draw(game._cells)
