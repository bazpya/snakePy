from src.game.cell import Cell
from src.game.snake import Snake
from tests.game.snake_ import Snake_sync_


class Snake_init_(Snake_sync_):
    def test_init_sets_one_cell_only(self):
        cell = Cell()
        sut = Snake(cell)
        self.assertEqual(1, sut.get_length())
