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
        up_neighbour = Cell(None, None)
        right_neighbour = Cell(None, None)
        down_neighbour = Cell(None, None)
        left_neighbour = Cell(None, None)

        neighbours = {
            Direction.up: up_neighbour,
            Direction.right: right_neighbour,
            Direction.down: down_neighbour,
            Direction.left: left_neighbour,
        }

        def side_effect_func(dir: Direction):
            return neighbours[dir]

        head = Cell(None, None)
        head.get_neighbour = side_effect_func
        worm = Worm(head)
        worm.step(Direction.up)
        self.assertEqual(up_neighbour, worm._head)
