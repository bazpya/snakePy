from src.game.cell import Cell
from src.game.snake import Snake
from src.game_test.snake_ import Snake_


class Snake_init_(Snake_):
    def test_init_sets_one_cell_only(self):
        cell = Cell()
        sut = Snake(cell)
        self.assertEqual(1, sut.get_length())
