import tensorflow as tf
from tests.ml.player_ import Player_
from src.game.direction import Turn


class Player_decide_(Player_):
    def _make_func(self, output: []):
        return lambda *args, **kwargs: [tf.constant(output)]

    def test_decide_returns_a_turn(self):
        sut = self.make_sut()
        eye_output = tf.random.normal([sut._eye.view_size])
        sut._eye.set_output(eye_output)
        self.assertIsInstance(sut.decide(), Turn)

    def test_decide_takes_left(self):
        sut = self.make_sut()
        eye_output = tf.random.normal([sut._eye.view_size])
        sut._eye.set_output(eye_output)
        sut._brain.predict = self._make_func([0.3, 0.2, 0.1])
        self.assertEqual(sut.decide(), Turn.left)

    def test_decide_goes_ahead(self):
        sut = self.make_sut()
        eye_output = tf.random.normal([sut._eye.view_size])
        sut._eye.set_output(eye_output)
        sut._brain.predict = self._make_func([0.1, 0.3, 0.1])
        self.assertEqual(sut.decide(), Turn.ahead)

    def test_decide_takes_right(self):
        sut = self.make_sut()
        eye_output = tf.random.normal([sut._eye.view_size])
        sut._eye.set_output(eye_output)
        sut._brain.predict = self._make_func([0.1, 0.2, 0.3])
        self.assertEqual(sut.decide(), Turn.right)
