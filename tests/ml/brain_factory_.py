import tensorflow as tf
from src.ml.brain_factory import BrainFactory
from tests.ml import test_ml_
from tests.test_ import Test_


class Brain_factory_(Test_):
    def test_makes_correct_type_of_model(self):
        res = BrainFactory.make(self.some, self.few)
        self.assertIsInstance(res, tf.keras.Sequential)

    def test_makes_correct_number_of_layers(self):
        res = BrainFactory.make(self.some, self.few)
        expected = len(BrainFactory.model_params.layer_sizes) + 1
        actual = len(res.layers)
        self.assertEqual(actual, expected)

    def test_makes_correct_layer_sizes(self):
        res = BrainFactory.make(self.some, self.few)
        for i, size in enumerate(BrainFactory.model_params.layer_sizes):
            layer = res.layers[i]
            self.assertEqual(layer.units, size)

    def test_makes_correct_output_layer_size(self):
        res = BrainFactory.make(self.some, self.few)
        last_layer = res.layers[-1]
        actual = last_layer.units
        expected = self.few
        self.assertEqual(actual, expected)
