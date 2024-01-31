import tensorflow as tf
from src.ml.view import View
from src.game.cell import Cell


class EyeFake:
    def __init__(self, view: View) -> None:
        self._view = view
        self.view_size: int = view.size
        self._output: tf.Tensor = None

    def see(self, head: Cell, food: Cell) -> tf:
        if self._output is None:
            return tf.random.normal([self.view_size])
        else:
            return self._output

    def set_output(self, output: tf.Tensor):
        self._output = output
