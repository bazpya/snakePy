import random
from src.ml.eye import Eye
from src.ml.player import PlayerResult
from src.game.result import GameResult
from src.game.event_hub import EventHub
from src.game.game import Game
from src.game.direction import Turn


class PlayerFake:
    _game: Game
    _id: int
    events: EventHub
    _eye: Eye = None

    def __init__(self, id: int, game: Game, eye: Eye) -> None:
        self._game = game
        self._id = id
        self._eye = eye
        self.events = EventHub()
        self.bind(game)

    def bind(self, game: Game) -> None:
        game.events.stepped.subscribe(self._on_stepped)
        game.events.died.subscribe(self._on_died)

    def _on_stepped(self, *args, **kwargs) -> None:
        self.send_game_input()

    def _on_died(self, game_res: GameResult) -> None:
        res = PlayerResult(self._id, self.get_fitness(game_res), game_res)
        self.events.died.emit(res)

    def send_game_input(self) -> None:
        turn = self.decide(self._game)
        self._game.turn(turn)

    def play_sync(self) -> None:
        self._game.run_sync()

    async def play_async(self, interval: float) -> None:
        await self._game.run_async(interval)

    def decide(self, *args, **kwargs) -> Turn:
        return random.choice(list(Turn))

    def clone(self, id: int, game: Game, eye: Eye) -> "PlayerFake":
        return PlayerFake(id, game, eye)

    def get_fitness(self, game_res: GameResult) -> float:
        return (
            game_res.snake.length
            + game_res.snake.steps_taken / 50
            + game_res.snake.cells_visited / (game_res.row_count * game_res.col_count)
        )
