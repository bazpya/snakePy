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

    def test_init_creates_cell_instances(self):
        for r in range(row_count):
            for c in range(col_count):
                self.assertIsInstance(sut._cells[r][c], Cell)

    def test_middle_cells_have_all_neighbours(self):
        for r in range(1, row_count - 1):
            for c in range(1, col_count - 1):
                cell = sut._cells[r][c]
                for dir in Direction:
                    self.assertIsNotNone(cell.get_neighbour(dir))

    def test_first_row_lack_up_neighbours(self):
        first_row = sut._cells[0]
        for c in range(col_count):
            cell = first_row[c]
            self.assertIsNone(cell.get_neighbour(Direction.up))

    def test_iterate_cells_hits_all_cells(self):
        all_cells_count = row_count * col_count

        def bazfunc(accumulator, this_cell, *args, **kwargs):
            return accumulator + 1

        count = sut.iterate_cells(True, bazfunc, 0)
        self.assertEqual(all_cells_count, count)

    def test_iterate_cells_hits_interior_cells(self):
        interior_cells_count = (row_count - 2) * (col_count - 2)

        def bazfunc(accumulator, this_cell, *args, **kwargs):
            return accumulator + 1

        count = sut.iterate_cells(False, bazfunc, 0)
        self.assertEqual(interior_cells_count, count)
