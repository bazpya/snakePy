import unittest
from source.cell import CellType, Cell
from source.global_refs import Direction
from test.helper.path_factory import PathFactory


class Cell_factory_(unittest.TestCase):
    _map = {
        "b": CellType.blank,
        "f": CellType.food,
        "s": CellType.snake,
        "w": CellType.wall,
    }

    def test_single_cells(self):
        for key, val in self._map.items():
            res = PathFactory.make(key)
            self.assertEqual(res.get_type(), val)

    def test_multi(self):
        pattern = "bfswbbfsw"
        types = [
            CellType.blank,
            CellType.food,
            CellType.snake,
            CellType.wall,
            CellType.blank,
            CellType.blank,
            CellType.food,
            CellType.snake,
            CellType.wall,
        ]
        runner = PathFactory.make(pattern)
        for type in types:
            self.assertEqual(runner.get_type(), type)
            runner = runner.get_neighbour(Direction.left)
