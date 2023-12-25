import unittest
from source.cell import Cell
from source.game import Game

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
