import random
from src.ml.Result import PlayerResult
from src.game.Result import GameResult
from src.game.event_hub import EventHub
from src.game.game import Game
from src.game.direction import Turn


class PlayerFake:
    _game: Game
    _id: int
    events: EventHub

    def __init__(self, game: Game, id: int):
        self._game = game
        self._id = id
        self.events = EventHub()
        self.bind(game)

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

    def play_sync(self):
        self._game.run_sync()

    async def play_async(self, interval: float):
        await self._game.run_async(interval)

    def decide(self, *args, **kwargs) -> Turn:
        return random.choice(list(Turn))
