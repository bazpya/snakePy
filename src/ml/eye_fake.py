import tensorflow as tf
from src.ml.eye import Eye
from src.ml.view import View
from src.game.cell import Cell


class EyeFake(Eye):
    def __init__(self, view: View) -> None:
        super(EyeFake, self).__init__(view)
        self._output: tf.Tensor = None

    def see(self, head: Cell, food: Cell) -> tf:
        if self._output is None:
            return tf.random.normal([self.view_size])
        else:
            return self._output

    def set_output(self, output: tf.Tensor):
        self._output = output
