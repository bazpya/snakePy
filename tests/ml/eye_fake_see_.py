import tensorflow as tf
from src.game.cell import Cell
from src.ml.eye_fake import EyeFake
from src.ml.view import View
from tests.ml.eye_ import Eye_


class Eye_fake_see_(Eye_):
    def test_see_gets_tensor(self):
        view = View()
        sut = EyeFake(view)
        head = Cell()
        food = Cell()
        actual = sut.see(head, food)
        self.assertIsInstance(actual, tf.Tensor)

    def test_see_gets_the_right_shape(self):
        view = View(True, False, True, False, True)
        sut = EyeFake(view)
        head = Cell()
        food = Cell()
        actual = sut.see(head, food).shape
        self.assertEqual(actual, [view.size])

    def test_see_gets_preset_output(self):
        view = View(True, False, True, False, True)
        sut = EyeFake(view)
        head = Cell()
        food = Cell()
        expected = tf.random.normal([view.size])
        sut.set_output(expected)
        actual = sut.see(head, food)
        self.assertTensorEqual(actual, expected)

    def test_see_without_preset_output(self):
        view = View(True, False, True, False, True)
        sut = EyeFake(view)
        head = Cell()
        food = Cell()
        expected = tf.random.normal([view.size])
        actual = sut.see(head, food)
        self.assertTensorDifferent(actual, expected)
