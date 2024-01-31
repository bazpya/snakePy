import tensorflow as tf
from src.ml.view import View
from src.game.cell import Cell


class EyeFake:
    def __init__(self, view: View) -> None:
        self._view = view
        self.view_size: int = view.size

    def see(self, head: Cell, food: Cell) -> tf:
        inputTensor = tf.random.normal((self.view_size,))
        return inputTensor
