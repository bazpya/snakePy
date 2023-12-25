import unittest
from source.global_refs import Direction
from source.game import Game
from source.cell import Cell

rows = 7
cols = 8
sut = Game(rows, cols)


class Cell_(unittest.TestCase):
    def test_init_creates_correct_number_of_rows(self):
        self.assertEqual(rows, len(sut.__cells__))

    def test_init_creates_correct_number_of_columns(self):
        for r in range(rows):
            self.assertEqual(cols, len(sut.__cells__[r]))

    def test_init_creates_cell_instances(self):
        for r in range(rows):
            for c in range(cols):
                self.assertIsInstance(sut.__cells__[r][c], Cell)

    def test_middle_cells_have_all_neighbours(self):
        for r in range(1, rows - 1):
            for c in range(1, cols - 1):
                cell = sut.__cells__[r][c]
                for dir in Direction:
                    self.assertIsNotNone(cell.get_neighbour(dir))

    def test_first_row_lack_up_neighbours(self):
        first_row = sut.__cells__[0]
        for c in range(cols):
            cell = first_row[c]
            self.assertIsNone(cell.get_neighbour(Direction.up))
