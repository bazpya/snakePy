from source.cell import Cell
from source.snake import Snake
from test.test_snake_ import Snake_


class Snake_init_(Snake_):
    def test_init_sets_one_cell_only(self):
        cell = Cell(None, None)
        sut = Snake(cell)
        self.assertEqual(1, sut.get_length())
