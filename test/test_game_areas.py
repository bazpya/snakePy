import unittest
from source.global_refs import Direction, CellType
from source.game import Game
from source.cell import Cell
from test.test_game_ import Game_

row_count = 17
col_count = 18
initial_sut = Game(row_count, col_count)


class Game_areas_(Game_):
    def test_first_row_is_wall(self):
        first_row = initial_sut._cells[0]
        for cell in first_row:
            self.assertTrue(cell.is_wall)

    def test_last_row_is_wall(self):
        last_row = initial_sut._cells[-1]
        for cell in last_row:
            self.assertTrue(cell.is_wall)

    def test_first_col_is_wall(self):
        for r in range(row_count):
            cell = initial_sut._cells[r][0]
            self.assertTrue(cell.is_wall)

    def test_last_col_is_wall(self):
        for r in range(row_count):
            cell = initial_sut._cells[r][-1]
            self.assertTrue(cell.is_wall)

    def test_interior_cells_are_blank(self):
        def visit(cell, ri, ci, acc):
            self.assertTrue(cell.is_blank())

        initial_sut.iterate_cells(False, visit)
