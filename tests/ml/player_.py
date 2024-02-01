from src.ml.view import View
from src.ml.eye_fake import EyeFake
from tests.ml.test_ml_ import Test_ml_
import tensorflow as tf
from src.ml.player import Player
from src.anonym import Anonym


class Player_(Test_ml_):
    def make_sut(self):
        game = self.make_game()
        view = View(True, False, True, False, True)
        eye = EyeFake(view)
        return Player(1, game, eye)
