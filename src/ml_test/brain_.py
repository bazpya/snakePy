import unittest
from src.game.direction import Direction
from src.ml.brain import Brain


class Brain_(unittest.TestCase):
    def test_decide_returns_a_direction(self):
        sut = Brain()
        self.assertIsInstance(sut.decide(), Direction)
