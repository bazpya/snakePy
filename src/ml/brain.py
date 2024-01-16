import keras
from keras import layers
from src.game.global_refs import Anonym
from src.game.direction import Direction


class Brain:
    # _model

    def __init__(self, model_params: Anonym):
        model_layers = []
        input_layer = layers.Dense(
            units=model_params.layer_sizes[0],
            activation=model_params.activation,
            use_bias=model_params.use_bias,
            kernel_initializer=model_params.kernel_initialiser,
            bias_initializer=model_params.bias_initialiser,
            input_shape=(model_params.input_size,),
        )
        model_layers.append(input_layer)
        for size in model_params.layer_sizes[1:]:
            layer = layers.Dense(
                units=size,
                activation=model_params.activation,
                use_bias=model_params.use_bias,
                kernel_initializer=model_params.kernel_initialiser,
                bias_initializer=model_params.bias_initialiser,
            )
            model_layers.append(layer)
        self._model = keras.Sequential(model_layers)

    def decide(self) -> Direction:
        return Direction.down
