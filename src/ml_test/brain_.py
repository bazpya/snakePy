import unittest
import tensorflow as tf
from src.game.global_refs import Anonym
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
        for i, layer in enumerate(sut._model.layers):
            self.assertEqual(layer.units, self._model_params.layer_sizes[i])

    def test_decide_returns_a_direction(self):
        sut = Brain(self._model_params)
        self.assertIsInstance(sut.decide(), Direction)
