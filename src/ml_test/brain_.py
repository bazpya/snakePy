import unittest
import tensorflow as tf
from src.anonym import Anonym
from src.game.direction import Direction
from src.ml.brain import Brain


class Brain_(unittest.TestCase):
    _model_params = Anonym(
        input_size=10,
        layer_sizes=[2, 3, 4, 5],
        activation=tf.keras.activations.linear,
        kernel_initialiser=tf.keras.initializers.LecunNormal,
        use_bias=False,
        bias_initialiser=tf.keras.initializers.zeros,
    )

    def test_init_makes_correct_layer_sizes(self):
        sut = Brain(self._model_params)
        for i, size in enumerate(self._model_params.layer_sizes):
            layer = sut._model.layers[i]
            self.assertEqual(layer.units, size)

    def test_init_adds_correct_output_layer_size(self):
        sut = Brain(self._model_params)
        last_layer = sut._model.layers[-1]
        output_layer_size = last_layer.units
        self.assertEqual(output_layer_size, Brain._output_layer_size)

    def test_decide_returns_a_direction(self):
        sut = Brain(self._model_params)
        self.assertIsInstance(sut.decide(), Direction)
