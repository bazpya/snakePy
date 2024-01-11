from source.cell import CellType, Cell
from source.direction import Direction
from test.test_cell_ import Cell_


class Cell_init_(Cell_):
    def test_init_with_unspecified_type_defaults_to_blank(self):
        expected = CellType.blank
        sut = Cell()
        self.assertEqual(expected, sut._type)

    def test_init_with_specified_type_sets_type(self):
        expected = CellType.wall
        sut = Cell(None, None, expected)
        self.assertEqual(expected, sut._type)

    def test_init_sets_neighbours_to_none(self):
        sut = Cell()
        self.assertIsNone(sut.get_neighbour(Direction.right))
