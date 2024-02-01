from src.ml.eye import Eye
from src.ml.view import View
from tests.ml.player_ import Player_
import tensorflow as tf
from src.ml.player import Player


class Player_clone_(Player_):
    def test_clone_makes_correct_type(self):
        sut = self.make_sut()
        game = self.make_game()
        view = View(True, False, True, False, True)
        eye = Eye(view)
        clone = sut.clone(2, game, eye)
        self.assertIsInstance(clone, Player)

    def test_clone_makes_new_object(self):
        sut = self.make_sut()
        game = self.make_game()
        view = View(True, False, True, False, True)
        eye = Eye(view)
        clone = sut.clone(2, game, eye)
        self.assertNotEqual(sut, clone)
        self.assertNotEqual(sut._id, clone._id)
        self.assertNotEqual(sut._game, clone._game)
        self.assertNotEqual(sut._eye, clone._eye)
