import unittest
from source.global_refs import Direction, CellType
from source.cell import Cell
from source.worm import Worm


class Worm_(unittest.TestCase):
    def test_init_sets_one_cell_only(self):
        cell = Cell(None, None)
        sut = Worm(cell)
        self.assertEqual(1, sut.get_length())

    def test_step_moves_head(self):
        self.skipTest("todo")
