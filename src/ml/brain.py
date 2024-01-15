import tensorflow as tf
import keras
from keras import layers
from src.game.direction import Direction


class Brain:
    # _model

    def __init__(
        self,
        input_size: int,
        layer_sizes: list[int],
        # activation,
        # kernel_initialiser,
        # use_bias,
        # bias_initialiser,
    ):
        model_layers = []
        input_layer = layers.Dense(
            units=layer_sizes[0],
            # activation=activation,
            # use_bias=use_bias,
            # kernel_initializer=kernel_initialiser,
            # bias_initializer=bias_initialiser,
            input_shape=(input_size,),
        )
        model_layers.append(input_layer)
        for size in layer_sizes[1:]:
            layer = layers.Dense(
                units=size,
                # activation=activation,
                # use_bias=use_bias,
                # kernel_initializer=kernel_initialiser,
                # bias_initializer=bias_initialiser,
            )
            model_layers.append(layer)
        self._model = keras.Sequential(model_layers)

    def decide(self) -> Direction:
        return Direction.down
