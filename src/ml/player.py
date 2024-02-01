import tensorflow as tf
from src.ml.brain_factory import BrainFactory
from src.ml.eye import Eye
from src.ml.Result import PlayerResult
from src.game.Result import GameResult
from src.game.event_hub import EventHub
from src.game.game import Game
from src.game.direction import Turn


class Player:
    _game: Game
    _id: int
    events: EventHub
    _output_layer_size: int
    _brain: None
    _eye: Eye = None

    def __init__(self, id: int, game: Game, eye: Eye) -> None:
        self._game = game
        self._id = id
        self.events = EventHub()
        self._eye = eye
        self.bind(game)
        input_size = eye.view_size
        self._output_layer_size = len(Turn)
        self._brain = BrainFactory.make(input_size, self._output_layer_size)

    def bind(self, game: Game) -> None:
        game.events.stepped.subscribe(self._on_stepped)
        game.events.died.subscribe(self._on_died)

    def _on_stepped(self, *args, **kwargs) -> None:
        self.send_game_input()

    def _on_died(self, game_res: GameResult) -> None:
        res = PlayerResult(self._id, game_res)
        self.events.died.emit(res)

    def send_game_input(self) -> None:
        turn = self.decide()
        self._game.turn(turn)

    def decide(self) -> Turn:
        head = self._game.get_head()
        food = self._game.get_current_food()
        brain_input = self._eye.see(head, food)
        brain_output = self._brain.predict(brain_input)[0]
        index = tf.math.argmax(brain_output).numpy()
        shifted_index = index - 1
        return Turn(shifted_index)

    def play_sync(self) -> None:
        self._game.run_sync()

    async def play_async(self, interval: float) -> None:
        await self._game.run_async(interval)

    # todo: unit test
    def clone(self, id: int, game: Game, eye: Eye) -> "Player":
        player = Player(id, game, eye)
        brain = BrainFactory.clone(self._brain)
        player._brain = brain
        return player
