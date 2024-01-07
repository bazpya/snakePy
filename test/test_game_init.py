import unittest
from source.global_refs import Direction, CellType
from source.game import Game
from source.cell import Cell
from test.test_game_ import Game_

row_count = 17
col_count = 18
initial_sut = Game(row_count, col_count)


class Game_init_(Game_):
    def test_init_creates_correct_number_of_rows(self):
        self.assertEqual(row_count, len(initial_sut._cells))

    def test_init_creates_correct_number_of_columns(self):
        for r in range(row_count):
            self.assertEqual(col_count, len(initial_sut._cells[r]))

    def test_init_with_only_one_dimension_creates_square(self):
        sut = Game(row_count)
        self.assertEqual(row_count, sut._col_count)

    def test_init_creates_cell_instances(self):
        def visit(cell, *args, **kwargs):
            self.assertIsInstance(cell, Cell)

        initial_sut.iterate_cells(True, visit)
