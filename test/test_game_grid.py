import unittest
from source.global_refs import Direction, CellType
from source.game import Game
from source.cell import Cell

row_count = 17
col_count = 18
initial_sut = Game(row_count, col_count)


class Game_grid_(unittest.TestCase):
    def test_middle_cells_have_all_neighbours(self):
        def visit(cell, ri, ci, acc):
            for dir in Direction:
                self.assertIsNotNone(cell.get_neighbour(dir))

        initial_sut.iterate_cells(False, visit)

    def test_first_row_lack_up_neighbours(self):
        first_row = initial_sut._cells[0]
        for c in range(col_count):
            cell = first_row[c]
            self.assertIsNone(cell.get_neighbour(Direction.up))

    def test_first_row_have_down_neighbours(self):
        first_row = initial_sut._cells[0]
        for c in range(col_count):
            cell = first_row[c]
            self.assertIsNotNone(cell.get_neighbour(Direction.down))

    def test_last_row_have_up_neighbours(self):
        last_row = initial_sut._cells[-1]
        for c in range(col_count):
            cell = last_row[c]
            self.assertIsNotNone(cell.get_neighbour(Direction.up))

    def test_last_row_lack_down_neighbours(self):
        last_row = initial_sut._cells[-1]
        for c in range(col_count):
            cell = last_row[c]
            self.assertIsNone(cell.get_neighbour(Direction.down))

    def test_first_col_lack_left_neighbours(self):
        for r in range(row_count):
            cell = initial_sut._cells[r][0]
            self.assertIsNone(cell.get_neighbour(Direction.left))

    def test_first_col_have_right_neighbours(self):
        for r in range(row_count):
            cell = initial_sut._cells[r][0]
            self.assertIsNotNone(cell.get_neighbour(Direction.right))

    def test_last_col_have_left_neighbours(self):
        for r in range(row_count):
            cell = initial_sut._cells[r][-1]
            self.assertIsNotNone(cell.get_neighbour(Direction.left))

    def test_last_col_lack_right_neighbours(self):
        for r in range(row_count):
            cell = initial_sut._cells[r][-1]
            self.assertIsNone(cell.get_neighbour(Direction.right))
