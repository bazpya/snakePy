import unittest
import tensorflow as tf
from ml.player import Player
from src.anonym import Anonym


class Player_(unittest.TestCase):
    _model_params = Anonym(
        input_size=10,
        layer_sizes=[2, 3, 4, 5],
        activation=tf.keras.activations.linear,
        kernel_initialiser=tf.keras.initializers.LecunNormal,
        use_bias=False,
        bias_initialiser=tf.keras.initializers.zeros,
    )

    def _get_sut(self):
        return Player(self._model_params)
