from src.ml.ml import ML
from src.ml.player import Player
from tests.ml.player_ import Player_
from src.game.direction import Turn


class Player_decide_(Player_):
    def _make_tensor_getter(self, output: []):
        res = [ML.constant(output)]
        return self.make_getter(res)

    def test_decide_takes_a_turn(self):
        sut = Player(1)
        eye_output = ML.random.normal([sut._eye.view_size])
        sut._eye.see = self.make_getter(eye_output)
        self.assertIsInstance(sut.decide(), Turn)

    def test_decide_takes_left(self):
        sut = Player(1)
        eye_output = ML.random.normal([sut._eye.view_size])
        sut._eye.see = self.make_getter(eye_output)
        sut._brain.predict = self._make_tensor_getter([0.3, 0.2, 0.1])
        self.assertEqual(sut.decide(), Turn.left)

    def test_decide_goes_ahead(self):
        sut = Player(1)
        eye_output = ML.random.normal([sut._eye.view_size])
        sut._eye.see = self.make_getter(eye_output)
        sut._brain.predict = self._make_tensor_getter([0.1, 0.3, 0.1])
        self.assertEqual(sut.decide(), Turn.ahead)

    def test_decide_takes_right(self):
        sut = Player(1)
        eye_output = ML.random.normal([sut._eye.view_size])
        sut._eye.see = self.make_getter(eye_output)
        sut._brain.predict = self._make_tensor_getter([0.1, 0.2, 0.3])
        self.assertEqual(sut.decide(), Turn.right)
