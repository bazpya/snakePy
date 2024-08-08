from src.ml.ml import ML
from src.config import Config, config
from src.tree import Tree


class BrainFactory:
    spec = Tree()
    spec.layer_sizes = Config.parse_ints(config.ml.brain.layer_sizes)
    spec.activation = ML.keras.activations.linear
    spec.kernel_initialiser = ML.keras.initializers.LecunNormal
    spec.use_bias = False
    spec.bias_initialiser = ML.keras.initializers.RandomNormal

    @staticmethod
    def make(input_size: int, output_size: int) -> ML.keras.Sequential:
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
        return ML.keras.Sequential(model_layers)

    @staticmethod
    def make_layer(
        spec: Tree, size: int, input_size: int = None
    ) -> ML.keras.layers.Dense:
        if input_size:
            return ML.keras.layers.Dense(
                units=size,
                activation=spec.activation,
                use_bias=spec.use_bias,
                kernel_initializer=spec.kernel_initialiser,
                bias_initializer=spec.bias_initialiser,
                input_shape=(input_size,),
            )
        else:
            return ML.keras.layers.Dense(
                units=size,
                activation=spec.activation,
                use_bias=spec.use_bias,
                kernel_initializer=spec.kernel_initialiser,
                bias_initializer=spec.bias_initialiser,
            )

    @staticmethod
    def clone(original: ML.keras.Sequential) -> ML.keras.Sequential:
        clone = ML.keras.models.clone_model(original)
        clone.set_weights(original.get_weights())
        return clone
