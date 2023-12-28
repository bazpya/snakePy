import unittest
from unittest.mock import MagicMock, Mock
from source.global_refs import Direction, CellType
from source.cell import Cell
from source.worm import Worm


class Worm_(unittest.TestCase):
    def test_init_sets_one_cell_only(self):
        cell = Cell(None, None)
        sut = Worm(cell)
        self.assertEqual(1, sut.get_length())

    def test_step_moves_head(self):
        next_cell = Cell(None, None)
        head = Cell(None, None)
        head.get_neighbour = lambda whatever: next_cell
        worm = Worm(head)
        worm.step(Direction.up)
        self.assertEqual(next_cell, worm.get_head())

    def test_step_makes_new_cell_worm(self):
        next_cell = Cell(None, None)
        head = Cell(None, None)
        head.get_neighbour = lambda whatever: next_cell
        worm = Worm(head)
        worm.step(Direction.up)
        self.assertTrue(next_cell.is_worm)

    def test_step_when_into_blank_cell_keeps_length_same(self):
        next_cell = Cell(None, None)
        head = Cell(None, None)
        head.get_neighbour = lambda whatever: next_cell
        worm = Worm(head)
        worm.step(Direction.up)
        self.assertEqual(1, worm.get_length())

    def test_step_when_into_food_cell_increments_length(self):
        self.skipTest("Todo")
