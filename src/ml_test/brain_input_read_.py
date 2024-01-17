import tensorflow as tf
from src.ml_test.brain_input_ import BrainInput_
from src.ml.brain_input import BrainInput

input_size = 8


class BrainInput_read(BrainInput_):
    def test_read_gets_tensor(self):
        sut = BrainInput(input_size, None, None)
        actual = sut.read()
        self.assertIsInstance(actual, tf.Tensor)

    def test_read_gets_the_right_dimensions(self):
        sut = BrainInput(input_size, None, None)
        actual = sut.read().shape
        self.assertEqual(actual, [input_size])
