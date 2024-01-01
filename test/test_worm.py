import unittest
from unittest.mock import MagicMock
from source.global_refs import CellType
from source.cell import Cell
from source.worm import Worm


class Worm_(unittest.TestCase):
    def test_init_sets_one_cell_only(self):
        cell = Cell(None, None)
        sut = Worm(cell)
        self.assertEqual(1, sut.get_length())

    def test_step_moves_head(self):
        destination = Cell(None, None)
        initial_head = Cell(None, None)
        initial_head.get_neighbour = lambda whatever: destination
        worm = Worm(initial_head)
        worm.step()
        self.assertEqual(destination, worm.get_head())

    def test_step_makes_new_cell_worm(self):
        destination = Cell(None, None)
        initial_head = Cell(None, None)
        initial_head.get_neighbour = lambda whatever: destination
        worm = Worm(initial_head)
        worm.step()
        self.assertTrue(destination.is_worm)

    def test_step_when_into_blank_makes_tail_cell_blank(self):
        destination = Cell(None, None)
        initial_head = Cell(None, None)
        initial_head.get_neighbour = lambda whatever: destination
        worm = Worm(initial_head)
        initial_tail = worm.get_tail()
        worm.step()
        self.assertTrue(initial_tail.is_blank())

    def test_step_when_into_blank_keeps_length_same(self):
        destination = Cell(None, None)
        initial_head = Cell(None, None)
        initial_head.get_neighbour = lambda whatever: destination
        worm = Worm(initial_head)
        initial_length = worm.get_length()
        worm.step()
        self.assertEqual(initial_length, worm.get_length())

    def test_step_when_into_food_increments_length(self):
        destination = Cell(None, None, CellType.food)
        initial_head = Cell(None, None)
        initial_head.get_neighbour = lambda whatever: destination
        worm = Worm(initial_head)
        initial_length = worm.get_length()
        worm.step()
        self.assertEqual(initial_length + 1, worm.get_length())

    def test_step_when_into_wall_invokes_death_callback(self):
        destination = Cell(None, None, CellType.wall)
        initial_head = Cell(None, None)
        initial_head.get_neighbour = lambda whatever: destination
        death_callback = MagicMock()
        worm = Worm(initial_head, death_callback)
        worm.step()
        death_callback.assert_called()
