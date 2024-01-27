import tensorflow as tf
from tests.ml.eye_ import Eye_
from src.ml.eye import Eye

input_size = 8


class Eye_see_(Eye_):
    def test_read_gets_tensor(self):
        sut = Eye(input_size, None)
        actual = sut.see(None)
        self.assertIsInstance(actual, tf.Tensor)

    def test_read_gets_the_right_dimensions(self):
        sut = Eye(input_size, None)
        actual = sut.see(None).shape
        self.assertEqual(actual, [input_size])
