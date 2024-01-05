from source.cell import Cell
from source.worm import Worm
from test.test_worm_ import Worm_


class Worm_init_(Worm_):
    def test_init_sets_one_cell_only(self):
        cell = Cell(None, None)
        sut = Worm(cell)
        self.assertEqual(1, sut.get_length())
