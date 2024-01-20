from src.ml_test.player_ import Player_
from src.game.direction import Turn


class Player_decide_(Player_):
    def test_decide_returns_a_turn(self):
        sut = self._get_sut()
        self.assertIsInstance(sut.decide(), Turn)

    # def test_decide_takes_highest_output(self):
    #     sut = self._get_sut()
    #     func = lambda *args: False
    #     sut._model.predict = func
    #     self.assertTrue(sut._model.predict())
