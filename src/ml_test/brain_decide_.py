from src.ml_test.brain_ import Brain_
from src.game.direction import Direction


class Brain_decide_(Brain_):
    def test_decide_returns_a_direction(self):
        sut = self._get_sut()
        self.assertIsInstance(sut.decide(), Direction)

    def test_decide_takes_highest_output(self):
        sut = self._get_sut()
        func = lambda *args: False
        sut._model.predict = func
        self.assertTrue(sut._model.predict())
