import keras
from keras import layers
import tensorflow as tf
from src.ml.eye import Eye
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

    def __init__(self, id: int, model_params: Anonym, game: Game, eye: Eye):
        self._game = game
        self._id = id
        self.events = EventHub()
        model_layers = []
        self._input_size = model_params.input_size
        self.bind(game)

        input_layer = layers.Dense(  # Add input layer
            units=model_params.layer_sizes[0],
            activation=model_params.activation,
            use_bias=model_params.use_bias,
            kernel_initializer=model_params.kernel_initialiser,
            bias_initializer=model_params.bias_initialiser,
            input_shape=(model_params.input_size,),
        )
        model_layers.append(input_layer)

        for size in model_params.layer_sizes[1:]:  # Add middle layers
            layer = layers.Dense(
                units=size,
                activation=model_params.activation,
                use_bias=model_params.use_bias,
                kernel_initializer=model_params.kernel_initialiser,
                bias_initializer=model_params.bias_initialiser,
            )
            model_layers.append(layer)

        output_layer = layers.Dense(  # Add output layer
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

    def _on_stepped(self, *args, **kwargs):
        self.send_game_input()

    def _on_died(self, game_res: GameResult):
        res = PlayerResult(self._id, game_res)
        self.events.died.emit(res)

    def send_game_input(self):
        turn = self.decide(self._game)
        self._game.turn(turn)

    def decide(self, input: tf.Tensor) -> Turn:
        brain_output = self._model.predict(input)[0]
        index = tf.math.argmax(brain_output).numpy()
        shifted_index = index - 1
        return Turn(shifted_index)

    def play_sync(self):
        self._game.run_sync()

    async def play_async(self, interval: float):
        await self._game.run_async(interval)
