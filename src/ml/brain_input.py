import tensorflow as tf
from src.game.cell import Cell


class BrainInput:
    _cells: list[Cell]
    _converter: object
    _input_size: int

    def __init__(self, input_size: int, cells: list[Cell], converter: object) -> None:
        self._cells = cells
        self._converter = converter
        self._input_size = input_size

    def read(self):
        # inputTensor = tf.Tensor(range(0, 8), [1, self._inputSize])
        inputTensor = tf.constant(range(0, self._input_size))
        return inputTensor
