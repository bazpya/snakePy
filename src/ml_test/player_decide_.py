import tensorflow as tf
from src.ml_test.player_ import Player_
from src.game.direction import Turn


class Player_decide_(Player_):
    def _make_func(self, output: []):
        main = tf.constant(output)
        res_tensor = tf.stack([main, main])  # just add an extra dimension
        return lambda *args, **kwargs: res_tensor

    def test_decide_returns_a_turn(self):
        sut = self._get_sut()
        input = tf.zeros([1, sut._input_size])
        self.assertIsInstance(sut.decide(input), Turn)

    def test_decide_takes_left(self):
        sut = self._get_sut()
        sut._model.predict = self._make_func([0.3, 0.2, 0.1])
        input = tf.zeros([1, sut._input_size])
        self.assertEqual(sut.decide(input), Turn.left)

    def test_decide_goes_ahead(self):
        sut = self._get_sut()
        sut._model.predict = self._make_func([0.1, 0.3, 0.1])
        input = tf.zeros([1, sut._input_size])
        self.assertEqual(sut.decide(input), Turn.ahead)

    def test_decide_takes_right(self):
        sut = self._get_sut()
        sut._model.predict = self._make_func([0.1, 0.2, 0.3])
        input = tf.zeros([1, sut._input_size])
        self.assertEqual(sut.decide(input), Turn.right)
