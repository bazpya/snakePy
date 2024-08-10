import os
from src.ml.ml import ML
from src.config import Config, config
from src.tree import Tree
from bazpy.utc import Utc
from numpy.random import normal


class BrainFactory:
    spec = Tree()
    spec.layer_sizes = Config.parse_ints(config.ml.brain.layer_sizes)
    spec.activation = ML.keras.activations.linear
    spec.kernel_initialiser = ML.keras.initializers.LecunNormal
    spec.use_bias = False
    spec.bias_initialiser = ML.keras.initializers.RandomNormal
    _dir = config.ml.brain.save_dir

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

    # https://medium.com/adding-noise-to-network-weights-in-tensorflow/adding-noise-to-network-weights-in-tensorflow-fddc82e851cb#:~:text=Adding%20noise%3A%20method%201&text=In%20the%20same%20manor%20set_weight,value%20plus%20some%20noise%20vector.
    @staticmethod
    def mutate(original: ML.keras.Sequential) -> ML.keras.Sequential:
        clone = ML.keras.models.clone_model(original)
        clone.set_weights(original.get_weights())
        BrainFactory.add_noise(clone)
        return clone

    # def weight_perturbation(model):
    #     for layer in model.layers:
    #         trainable_weights = layer.trainable_variables

    #         for weight in trainable_weights:
    #             random_weights = tf.random.uniform(
    #                 tf.shape(weight), 1e-4, 1e-5, dtype=tf.float32
    #             )
    #             weight.assign_add(random_weights)

    @staticmethod
    def add_noise(model: ML.keras.Sequential) -> None:
        centre, std_deviation = 0.0, 1
        for layer_weights in model.trainable_weights:
            noise = normal(
                loc=centre,
                scale=std_deviation,
                size=layer_weights.shape,
            )
            layer_weights.assign_add(noise)

    @staticmethod
    def save(brain: ML.keras.Sequential) -> None:
        now = Utc.get_now()
        timestamp = now.strftime("%y%m%d-%H%M%S")
        filename = f"{BrainFactory._dir}brain-{timestamp}.keras"
        brain.save(filename)

    @staticmethod
    def load(filename: str = None, verbose: bool = False) -> ML.keras.Sequential:
        if filename:
            filepath = f"{BrainFactory._dir}{filename}"
        else:
            filepath = BrainFactory.get_latest_filepath()
        verbose and print(f"Read brain from: {filepath}")
        brain = ML.keras.models.load_model(filepath)
        return brain

    def get_latest_filepath() -> str:
        filenames = os.listdir(BrainFactory._dir)
        paths = [os.path.join(BrainFactory._dir, x) for x in filenames]
        latest = max(paths, key=os.path.getctime)
        return latest
