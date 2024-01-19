import keras
from keras import layers
from src.anonym import Anonym
from src.game.direction import Direction


class Brain:
    _output_layer_size: int = 3
    _model: None

    def __init__(self, model_params: Anonym):
        model_layers = []

        # Add input layer
        input_layer = layers.Dense(
            units=model_params.layer_sizes[0],
            activation=model_params.activation,
            use_bias=model_params.use_bias,
            kernel_initializer=model_params.kernel_initialiser,
            bias_initializer=model_params.bias_initialiser,
            input_shape=[model_params.input_size],
        )
        model_layers.append(input_layer)

        # Add middle layers
        for size in model_params.layer_sizes[1:]:
            layer = layers.Dense(
                units=size,
                activation=model_params.activation,
                use_bias=model_params.use_bias,
                kernel_initializer=model_params.kernel_initialiser,
                bias_initializer=model_params.bias_initialiser,
            )
            model_layers.append(layer)

        # Add output layer
        output_layer = layers.Dense(
            units=self._output_layer_size,
            activation=model_params.activation,
            use_bias=model_params.use_bias,
            kernel_initializer=model_params.kernel_initialiser,
            bias_initializer=model_params.bias_initialiser,
        )
        model_layers.append(output_layer)

        self._model = keras.Sequential(model_layers)

    def decide(self) -> Direction:
        return Direction.down

    # #getNextDirection() {
    #     const brainOutputTensor = this.#think();
    #     const brainOutputArray = brainOutputTensor.arraySync()[0];
    #     let indexOfMax = BazArray.getMax(brainOutputArray).index;
    #     if (indexOfMax === 0)
    #         return Direction.up;
    #     if (indexOfMax === 1)
    #         return Direction.right;
    #     if (indexOfMax === 2)
    #         return Direction.down;
    #     if (indexOfMax === 3)
    #         return Direction.left;
    # }

    # #think() {
    #     const me = this;
    #     const inputVector = this.#getInput();
    #     const brainOutput = tf.tidy(() => {
    #         const inputTensor = tf.tensor(inputVector, [1, me.#inputSize]);
    #         return me.#brain.predict(inputTensor, { batchSize: 1 });
    #     });
    #     return brainOutput;
    # }

    # #getInput() {
    #     let result = [];
    #     const foodDiffHor = The.grid.food.col - this.#head.col;
    #     const foodDiffVer = The.grid.food.row - this.#head.row;
    #     const foodSignalHor = foodDiffHor === 0 ? 0 : 1 / foodDiffHor;
    #     result.push(foodSignalHor);
    #     const foodSignalVer = foodDiffVer === 0 ? 0 : 1 / foodDiffVer;
    #     result.push(foodSignalVer);

    #     let deathVector = this.#head.getDiff(c => c.isDeadly, Direction.up);
    #     const deathSignalUp = - 1 / BazMath.amplitude(deathVector);
    #     result.push(deathSignalUp);

    #     deathVector = this.#head.getDiff(c => c.isDeadly, Direction.up, Direction.right);
    #     const deathSignalUpRight = - 1 / BazMath.amplitude(deathVector);
    #     result.push(deathSignalUpRight);

    #     deathVector = this.#head.getDiff(c => c.isDeadly, Direction.right);
    #     const deathSignalRight = - 1 / BazMath.amplitude(deathVector);
    #     result.push(deathSignalRight);

    #     deathVector = this.#head.getDiff(c => c.isDeadly, Direction.right, Direction.down);
    #     const deathSignalDownRight = - 1 / BazMath.amplitude(deathVector);
    #     result.push(deathSignalDownRight);

    #     deathVector = this.#head.getDiff(c => c.isDeadly, Direction.down);
    #     const deathSignalDown = - 1 / BazMath.amplitude(deathVector);
    #     result.push(deathSignalDown);

    #     deathVector = this.#head.getDiff(c => c.isDeadly, Direction.down, Direction.left);
    #     const deathSignalDownLeft = - 1 / BazMath.amplitude(deathVector);
    #     result.push(deathSignalDownLeft);

    #     deathVector = this.#head.getDiff(c => c.isDeadly, Direction.left);
    #     const deathSignalLeft = - 1 / BazMath.amplitude(deathVector);
    #     result.push(deathSignalLeft);

    #     deathVector = this.#head.getDiff(c => c.isDeadly, Direction.left, Direction.up);
    #     const deathSignalUpLeft = - 1 / BazMath.amplitude(deathVector);
    #     result.push(deathSignalUpLeft);

    #     return result;
    # }
