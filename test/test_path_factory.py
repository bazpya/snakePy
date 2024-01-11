import unittest
from source.cell import CellType
from source.direction import Direction
from test.helper.path_factory import PathFactory


class Path_factory_(unittest.TestCase):
    _map = {
        "b": CellType.blank,
        "f": CellType.food,
        "s": CellType.snake,
        "w": CellType.wall,
    }

    # ======================  Make List  ======================
    def test_make_list_gets_right_number_of_cells(self):
        res = PathFactory.make_list("bfsw")
        self.assertEqual(len(res), 4)

    def test_make_list_gets_right_type_of_cells(self):
        res = PathFactory.make_list("bfsw")
        self.assertEqual(res[0].get_type(), CellType.blank)
        self.assertEqual(res[1].get_type(), CellType.food)
        self.assertEqual(res[2].get_type(), CellType.snake)
        self.assertEqual(res[3].get_type(), CellType.wall)

    # ======================  Link  ======================

    def test_link_works(self):
        cells = PathFactory.make_list("bfswbfswbfsw")
        chain = PathFactory.link(cells)
        for i, cell in enumerate(cells[:-1]):
            next = cells[i + 1]
            self.assertEqual(cell.get_neighbour(Direction.left), next)

    # ======================  Make Chain  ======================

    def test_make_chain_single_cells(self):
        for key, val in self._map.items():
            res = PathFactory.make_chain(key)
            self.assertEqual(res.get_type(), val)

    def test_make_chain_multi(self):
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
        runner = PathFactory.make_chain(pattern)
        for type in types:
            self.assertEqual(runner.get_type(), type)
            runner = runner.get_neighbour(Direction.left)
