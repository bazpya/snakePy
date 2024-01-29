import keras
from keras import layers
import tensorflow as tf
from src.ml.Result import PlayerResult
from src.game.Result import GameResult
from src.game.event_hub import EventHub
from src.game.game import Game
from src.anonym import Anonym
from src.game.direction import Turn


class Player:
    _game: Game
    _id: int
    events: EventHub
    _output_layer_size: int = 3
    _model: None
    _input_size: int

    def __init__(self, game: Game, id: int, model_params: Anonym):
        self._game = game
        self._id = id
        self.events = EventHub()
        model_layers = []
        self._input_size = model_params.input_size
        self.bind(game)

        # Add input layer
        input_layer = layers.Dense(
            units=model_params.layer_sizes[0],
            activation=model_params.activation,
            use_bias=model_params.use_bias,
            kernel_initializer=model_params.kernel_initialiser,
            bias_initializer=model_params.bias_initialiser,
            input_shape=(model_params.input_size,),
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

    def bind(self, game: Game):
        game.events.stepped.subscribe(self._on_stepped)
        game.events.died.subscribe(self._on_died)

    def decide(self, input: tf.Tensor) -> Turn:
        brain_output = self._model.predict(input)[0]
        index = tf.math.argmax(brain_output).numpy()
        shifted_index = index - 1
        return Turn(shifted_index)

    def _on_stepped(self, *args, **kwargs):
        self.send_game_input()

    def _on_died(self, game_res: GameResult):
        res = PlayerResult(self._id, game_res)
        self.events.died.emit(res)

    def send_game_input(self):
        turn = self.decide(self._game)
        self._game.turn(turn)

    def play_sync(self):
        self._game.run_sync()

    async def play_async(self, interval: float):
        await self._game.run_async(interval)

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
