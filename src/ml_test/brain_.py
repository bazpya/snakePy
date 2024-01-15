import unittest
from src.game.direction import Direction
from src.ml.brain import Brain


class Brain_(unittest.TestCase):
    _sizes = [2, 3, 4, 5]
    _input_size = 10

    def test_init_makes_correct_layer_sizes(self):
        sut = Brain(input_size=8, layer_sizes=self._sizes)
        for i, layer in enumerate(sut._model.layers):
            self.assertEqual(layer.units, self._sizes[i])

    def test_decide_returns_a_direction(self):
        sut = Brain(self._input_size, [2, 3, 4, 5])
        self.assertIsInstance(sut.decide(), Direction)
