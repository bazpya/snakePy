import unittest
from source.global_refs import Direction
from source.game import Game
from source.cell import Cell

row_count = 7
col_count = 8
sut = Game(row_count, col_count)


class Cell_(unittest.TestCase):
    def test_init_creates_correct_number_of_rows(self):
        self.assertEqual(row_count, len(sut._cells))

    def test_init_creates_correct_number_of_columns(self):
        for r in range(row_count):
            self.assertEqual(col_count, len(sut._cells[r]))

    def test_iterate_cells_hits_all_cells(self):
        all_cells_count = row_count * col_count

        def counter_func(cell, ri, ci, acc):
            return acc + 1

        count = sut.iterate_cells(True, counter_func, 0)
        self.assertEqual(all_cells_count, count)

    def test_iterate_cells_hits_interior_cells(self):
        interior_cells_count = (row_count - 2) * (col_count - 2)

        def counter_func(cell, ri, ci, acc):
            return acc + 1

        count = sut.iterate_cells(False, counter_func, 0)
        self.assertEqual(interior_cells_count, count)

    def test_init_creates_cell_instances(self):
        def visit(cell, *args, **kwargs):
            self.assertIsInstance(cell, Cell)

        sut.iterate_cells(True, visit)

    def test_middle_cells_have_all_neighbours(self):
        def visit(cell, ri, ci, acc):
            for dir in Direction:
                self.assertIsNotNone(cell.get_neighbour(dir))

        sut.iterate_cells(False, visit)

    # ==========================================

    def test_first_row_lack_up_neighbours(self):
        first_row = sut._cells[0]
        for c in range(col_count):
            cell = first_row[c]
            self.assertIsNone(cell.get_neighbour(Direction.up))

    def test_first_row_have_down_neighbours(self):
        first_row = sut._cells[0]
        for c in range(col_count):
            cell = first_row[c]
            self.assertIsNotNone(cell.get_neighbour(Direction.down))

    def test_last_row_have_up_neighbours(self):
        last_row = sut._cells[-1]
        for c in range(col_count):
            cell = last_row[c]
            self.assertIsNotNone(cell.get_neighbour(Direction.up))

    def test_last_row_lack_down_neighbours(self):
        last_row = sut._cells[-1]
        for c in range(col_count):
            cell = last_row[c]
            self.assertIsNone(cell.get_neighbour(Direction.down))

    # ==========================================

    def test_first_col_lack_left_neighbours(self):
        for r in range(row_count):
            cell = sut._cells[r][0]
            self.assertIsNone(cell.get_neighbour(Direction.left))

    def test_first_col_have_right_neighbours(self):
        for r in range(row_count):
            cell = sut._cells[r][0]
            self.assertIsNotNone(cell.get_neighbour(Direction.right))

    def test_last_col_have_left_neighbours(self):
        for r in range(row_count):
            cell = sut._cells[r][-1]
            self.assertIsNotNone(cell.get_neighbour(Direction.left))

    def test_last_col_lack_right_neighbours(self):
        for r in range(row_count):
            cell = sut._cells[r][-1]
            self.assertIsNone(cell.get_neighbour(Direction.right))
