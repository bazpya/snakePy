import tensorflow as tf
from src.game.game import Game
from src.game.cell import Cell


class Eye:
    def __init__(self, game: Game) -> None:
        self._game = game
        self._input_size = 8

    def see(self):
        # inputTensor = tf.Tensor(range(0, 8), [1, self._inputSize])
        inputTensor = tf.constant(range(0, self._input_size))
        return inputTensor
