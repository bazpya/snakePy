from src.game.game import Game
from tests.test_ import Test_


class Test_ml_(Test_):
    def make_game(self):
        return Game(self.many, self.many)
