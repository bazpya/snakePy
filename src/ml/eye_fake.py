import tensorflow as tf
from src.ml.sight import Sight
from src.game.cell import Cell


class EyeFake:
    def __init__(self, sight: Sight) -> None:
        self._sight = sight

    def see(self, head: Cell, food: Cell) -> tf:
        inputTensor = tf.random.normal((self._sight.size,))
        return inputTensor
