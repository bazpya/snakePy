from tests.ml.test_ml_ import Test_ml_
import tensorflow as tf
from src.ml.eye import Eye


class Eye_(Test_ml_):
    def test_read_gets_tensor(self):
        sut = Eye(self.few, None)
        actual = sut.see(None)
        self.assertIsInstance(actual, tf.Tensor)

    def test_read_gets_the_right_dimensions(self):
        sut = Eye(self.few, None)
        actual = sut.see(None).shape
        self.assertEqual(actual, [self.few])
