from src.game.game import Game
from src.game.cell import Cell
from tests.game.game_ import Game_


class Game_init_(Game_):
    def test_init_creates_correct_number_of_rows(self):
        self.assertEqual(self.row_count, len(self._sut._cells))

    def test_init_creates_correct_number_of_columns(self):
        for r in range(self.row_count):
            self.assertEqual(self.col_count, len(self._sut._cells[r]))

    def test_init_with_only_one_dimension_creates_square(self):
        sut = Game(self.row_count)
        self.assertEqual(self.row_count, sut.col_count)

    def test_init_creates_cell_instances(self):
        def visit(cell, *args, **kwargs):
            self.assertIsInstance(cell, Cell)

        self._sut.iterate_cells(True, visit)
