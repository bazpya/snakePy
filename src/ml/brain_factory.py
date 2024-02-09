import keras
from keras import layers
import tensorflow as tf
from src.config import Config, config
from src.tree import Tree


class BrainFactory:
    spec = Tree()
    spec.layer_sizes = Config.parse_ints(config.ml.brain.layer_sizes)
    spec.activation = tf.keras.activations.linear
    spec.kernel_initialiser = tf.keras.initializers.LecunNormal
    spec.use_bias = False
    spec.bias_initialiser = tf.keras.initializers.RandomNormal

    @staticmethod
    def make(input_size: int, output_size: int) -> keras.Sequential:
        s = BrainFactory.spec
        model_layers = []

        # Add input layer
        input_layer_size = s.layer_sizes[0]
        input_layer = BrainFactory.make_layer(s, input_layer_size, input_size)
        model_layers.append(input_layer)

        # Add middle layers
        for size in s.layer_sizes[1:]:
            layer = BrainFactory.make_layer(s, size)
            model_layers.append(layer)

        # Add output layer
        output_layer = BrainFactory.make_layer(s, output_size)
        model_layers.append(output_layer)
        return keras.Sequential(model_layers)

    @staticmethod
    def make_layer(spec: Tree, size: int, input_size: int = None) -> keras.layers.Dense:
        if input_size:
            return layers.Dense(
                units=size,
                activation=spec.activation,
                use_bias=spec.use_bias,
                kernel_initializer=spec.kernel_initialiser,
                bias_initializer=spec.bias_initialiser,
                input_shape=(input_size,),
            )
        else:
            return layers.Dense(
                units=size,
                activation=spec.activation,
                use_bias=spec.use_bias,
                kernel_initializer=spec.kernel_initialiser,
                bias_initializer=spec.bias_initialiser,
            )

    @staticmethod
    def clone(original: keras.Sequential) -> keras.Sequential:
        clone = keras.models.clone_model(original)
        clone.set_weights(original.get_weights())
        return clone
