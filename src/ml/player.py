import asyncio
import tensorflow as tf
from src.ml.brain_factory import BrainFactory
from src.ml.eye import Eye
from src.game.result import GameResult
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

    def __init__(self, id: int, game: Game = None, eye: Eye = None) -> None:
        self._game = game if game else Game()
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
        res = PlayerResult(self, self.get_fitness(game_res), game_res)
        self.events.died.emit(res)

    def send_game_input(self) -> None:
        turn = self.decide()
        self._game.turn(turn)

    def decide(self) -> Turn:
        head = self._game.get_head()
        food = self._game.get_current_food()
        eye_output = self._eye.see(head, food)
        brain_input = eye_output[None, ...]  # just add an extra dimension
        brain_output = self._brain.predict(brain_input)[0]
        index = tf.math.argmax(brain_output).numpy()
        shifted_index = index - 1
        return Turn(shifted_index)

    def play_sync(self) -> None:
        self._game.run_sync()

    async def play_awaitable_sync(self) -> None:
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self.play_sync)

    async def play_async(self, interval: float) -> None:
        await self._game.run_async(interval)

    def clone(self, id: int, game: Game, eye: Eye) -> "Player":
        player = Player(id, game, eye)
        brain = BrainFactory.clone(self._brain)
        player._brain = brain
        return player

    def get_fitness(self, game_res: GameResult) -> float:
        # fitness() { return this.#age + (this.length - 1) * The.grid.playableCellCount }
        return (
            game_res.snake.length
            + game_res.snake.steps_taken / 50
            + game_res.snake.cells_visited / (game_res.row_count * game_res.col_count)
        )

    def serialise(self):
        return f"Player-{self._id}"


class PlayerResult(GameResult):
    def __init__(
        self,
        player: Player,
        fitness: float,
        game_res: GameResult,
    ) -> None:
        self.player = player
        self.fitness = fitness
        self.game = game_res
