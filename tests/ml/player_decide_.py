import tensorflow as tf
from tests.ml.player_ import Player_
from src.game.direction import Turn


class Player_decide_(Player_):
    def _make_func(self, output: []):
        main = tf.constant(output)
        res_tensor = tf.stack([main, main])  # just add an extra dimension
        return lambda *args, **kwargs: res_tensor

    def test_decide_returns_a_turn(self):
        sut = self.make_sut()
        brain_input = tf.random.normal([1, sut._input_size])
        sut._eye.set_output(brain_input)
        self.assertIsInstance(sut.decide(), Turn)

    def test_decide_takes_left(self):
        sut = self.make_sut()
        brain_input = tf.random.normal([1, sut._input_size])
        sut._eye.set_output(brain_input)
        sut._model.predict = self._make_func([0.3, 0.2, 0.1])
        self.assertEqual(sut.decide(), Turn.left)

    def test_decide_goes_ahead(self):
        sut = self.make_sut()
        brain_input = tf.random.normal([1, sut._input_size])
        sut._eye.set_output(brain_input)
        sut._model.predict = self._make_func([0.1, 0.3, 0.1])
        self.assertEqual(sut.decide(), Turn.ahead)

    def test_decide_takes_right(self):
        sut = self.make_sut()
        brain_input = tf.random.normal([1, sut._input_size])
        sut._eye.set_output(brain_input)
        sut._model.predict = self._make_func([0.1, 0.2, 0.3])
        self.assertEqual(sut.decide(), Turn.right)
