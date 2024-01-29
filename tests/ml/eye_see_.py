import tensorflow as tf
from tests.ml.eye_ import Eye_
from src.ml.eye import Eye

input_size = 8


class Eye_see_(Eye_):
    def test_see_gets_tensor(self):
        game = self.make_game()
        sut = Eye(game)
        actual = sut.see()
        self.assertIsInstance(actual, tf.Tensor)

    # def test_read_gets_the_right_dimensions(self):
    #     game = self.make_game()
    #     sut = Eye(game)
    #     actual = sut.see().shape
    #     self.assertEqual(actual, [input_size])
