import unittest
from source.global_refs import Direction, CellType
from source.game import Game
from source.cell import Cell

row_count = 17
col_count = 18
initial_sut = Game(row_count, col_count)


class Cell_(unittest.TestCase):
    def test_init_creates_correct_number_of_rows(self):
        self.assertEqual(row_count, len(initial_sut._cells))

    def test_init_creates_correct_number_of_columns(self):
        for r in range(row_count):
            self.assertEqual(col_count, len(initial_sut._cells[r]))

    def test_iterate_cells_hits_all_cells(self):
        all_cells_count = row_count * col_count

        def counter_func(cell, ri, ci, acc):
            return acc + 1

        count = initial_sut.iterate_cells(True, counter_func, 0)
        self.assertEqual(all_cells_count, count)

    def test_iterate_cells_hits_interior_cells(self):
        interior_cells_count = (row_count - 2) * (col_count - 2)

        def counter_func(cell, ri, ci, acc):
            return acc + 1

        count = initial_sut.iterate_cells(False, counter_func, 0)
        self.assertEqual(interior_cells_count, count)

    def test_init_creates_cell_instances(self):
        def visit(cell, *args, **kwargs):
            self.assertIsInstance(cell, Cell)

        initial_sut.iterate_cells(True, visit)

    def test_middle_cells_have_all_neighbours(self):
        def visit(cell, ri, ci, acc):
            for dir in Direction:
                self.assertIsNotNone(cell.get_neighbour(dir))

        initial_sut.iterate_cells(False, visit)

    # ==========================================

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

    # ==========================================

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

    # ==========================================

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

    # ==========================================

    def test_get_blank_cells_gets_blanks(self):
        actual = initial_sut._get_blank_cells()
        for cell in actual:
            self.assertTrue(cell.is_blank())

    def test_get_blank_cells_gets_correct_number_of_cells(self):
        supposed_blanks = initial_sut._get_blank_cells()
        count = len(supposed_blanks)
        self.assertEqual((row_count - 2) * (col_count - 2), count)

    def test_drop_food_affects_one_cell(self):
        sut = Game(row_count, col_count)
        food_cell = sut._drop_food()

        def counter_func(cell, ri, ci, acc):
            return acc + 1 if cell.is_food() else acc

        count = sut.iterate_cells(False, counter_func, 0)
        self.assertEqual(1, count)
