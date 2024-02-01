from src.ml.player_fake import PlayerFake
from src.ml.view import View
from src.ml.eye_fake import EyeFake
from tests.ml.test_ml_ import Test_ml_


class Player_fake_(Test_ml_):
    def make_sut(self):
        game = self.make_game()
        view = View(True, False, True, False, True)
        eye = EyeFake(view)
        return PlayerFake(1, game, eye)

    def test_clone_makes_correct_type(self):
        sut = self.make_sut()
        game = self.make_game()
        view = View(True, False, True, False, True)
        eye = EyeFake(view)
        clone = sut.clone(2, game, eye)
        self.assertIsInstance(clone, PlayerFake)

    def test_clone_makes_new_object(self):
        sut = self.make_sut()
        game = self.make_game()
        view = View(True, False, True, False, True)
        eye = EyeFake(view)
        clone = sut.clone(2, game, eye)
        self.assertNotEqual(sut, clone)
        self.assertNotEqual(sut._id, clone._id)
        self.assertNotEqual(sut._game, clone._game)
        self.assertNotEqual(sut._eye, clone._eye)
