from tests.ml.player_ import Player_
from src.ml.player import Player


class Player_clone_(Player_):
    def test_clone_makes_correct_type(self):
        sut = Player(1)
        clone = sut.clone(2)
        self.assertIsInstance(clone, Player)

    def test_clone_makes_new_object(self):
        sut = Player(1)
        clone = sut.clone(2)
        self.assertNotEqual(sut, clone)
        self.assertNotEqual(sut._id, clone._id)
        self.assertNotEqual(sut._game, clone._game)
        self.assertNotEqual(sut._eye, clone._eye)
