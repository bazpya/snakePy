import random
from src.game.direction import Turn


class PlayerFake:
    def __init__(self, *args, **kwargs):
        pass

    def decide(self, *args, **kwargs) -> Turn:
        return random.choice(list(Turn))
