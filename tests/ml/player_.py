from src.ml.view import View
from src.ml.eye_fake import EyeFake
from tests.ml.test_ml_ import Test_ml_
import tensorflow as tf
from src.ml.player import Player
from src.anonym import Anonym


class Player_(Test_ml_):
    _model_params = Anonym(
        input_size=10,
        layer_sizes=[2, 3, 4, 5],
        activation=tf.keras.activations.linear,
        kernel_initialiser=tf.keras.initializers.LecunNormal,
        use_bias=False,
        bias_initialiser=tf.keras.initializers.RandomNormal,
    )

    def make_sut(self):
        game = self.make_game()
        view = View(True, False, True, False, True)
        eye = EyeFake(view)
        return Player(1, self._model_params, game, eye)
