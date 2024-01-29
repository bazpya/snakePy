import tensorflow as tf
from src.ml.sight import Sight
from tests.ml.eye_ import Eye_
from src.ml.eye import Eye


class Eye_see_(Eye_):
    def test_see_gets_tensor(self):
        game = self.make_game()
        sight = Sight()
        sut = Eye(game, sight)
        actual = sut.see()
        self.assertIsInstance(actual, tf.Tensor)

    def test_read_gets_the_right_shape(self):
        game = self.make_game()
        sight = Sight(True, False, True, False, True)
        sut = Eye(game, sight)
        actual = sut.see().shape
        self.assertEqual(actual, [sight.size])
