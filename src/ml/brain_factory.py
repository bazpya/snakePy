import keras
from keras import layers
import tensorflow as tf
from src.config import Config
from src.anonym import Anonym


class BrainFactory:
    model_params = Anonym(
        layer_sizes=Config.parse_ints(Config.get().ml.brain.layer_sizes),
        activation=tf.keras.activations.linear,
        kernel_initialiser=tf.keras.initializers.LecunNormal,
        use_bias=False,
        bias_initialiser=tf.keras.initializers.RandomNormal,
    )

    @staticmethod
    def make(input_size: int, output_size: int) -> keras.Sequential:
        model_params = BrainFactory.model_params
        model_layers = []

        # Add input layer
        input_layer_size = model_params.layer_sizes[0]
        input_layer = BrainFactory.make_layer(
            model_params, input_layer_size, input_size
        )
        model_layers.append(input_layer)

        # Add middle layers
        for size in model_params.layer_sizes[1:]:
            layer = BrainFactory.make_layer(model_params, size)
            model_layers.append(layer)

        # Add output layer
        output_layer = BrainFactory.make_layer(model_params, output_size)
        model_layers.append(output_layer)
        return keras.Sequential(model_layers)

    @staticmethod
    def make_layer(
        params: Anonym, size: int, input_size: int = None
    ) -> keras.layers.Dense:
        if input_size:
            return layers.Dense(
                units=size,
                activation=params.activation,
                use_bias=params.use_bias,
                kernel_initializer=params.kernel_initialiser,
                bias_initializer=params.bias_initialiser,
                input_shape=(input_size,),
            )
        else:
            return layers.Dense(
                units=size,
                activation=params.activation,
                use_bias=params.use_bias,
                kernel_initializer=params.kernel_initialiser,
                bias_initializer=params.bias_initialiser,
            )

    @staticmethod
    def clone(original: keras.Sequential) -> keras.Sequential:
        clone = keras.models.clone_model(original)
        clone.set_weights(original.get_weights())
        return clone
