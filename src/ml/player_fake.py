import random
from src.game.game import Game
from src.game.direction import Turn


class PlayerFake:
    _game: Game

    def __init__(self, game: Game, *args, **kwargs):
        self._game = game
        game.events.stepped.subscribe(self.send_game_input)

    def decide(self, *args, **kwargs) -> Turn:
        return random.choice(list(Turn))

    def send_game_input(self, *args, **kwargs):
        turn = self.decide(self._game)
        self._game.turn(turn)

    def play_sync(self):
        self._game.run_sync()

    async def play_async(self, interval: float):
        await self._game.run_async(interval)
