import unittest
from source.cell import CellType, Cell
from source.global_refs import Direction


class Cell_(unittest.TestCase):
    def test_init_with_unspecified_type_defaults_to_blank(self):
        expected = CellType.blank
        sut = Cell(None, None)
        self.assertEqual(expected, sut._type)

    def test_init_with_specified_type_sets_type(self):
        expected = CellType.wall
        sut = Cell(None, None, expected)
        self.assertEqual(expected, sut._type)

    def test_getter_and_attribute_return_same(self):
        expected = CellType.worm
        sut = Cell(None, None, expected)
        self.assertEqual(sut.get_type(), sut._type)

    def test_be_wall_makes_wall(self):
        sut = Cell(None, None)
        sut.be_wall()
        self.assertEqual(CellType.wall, sut.get_type())

    def test_be_worm_makes_worm(self):
        sut = Cell(None, None)
        sut.be_worm()
        self.assertEqual(CellType.worm, sut.get_type())

    def test_be_food_makes_food(self):
        sut = Cell(None, None)
        sut.be_food()
        self.assertEqual(CellType.food, sut.get_type())

    def test_be_blank_makes_blank(self):
        sut = Cell(None, None, CellType.food)
        sut.be_blank()
        self.assertEqual(CellType.blank, sut.get_type())

    def test_init_sets_neighbours_to_none(self):
        sut = Cell(None, None)
        self.assertIsNone(sut.get_neighbour(Direction.right))

    def test_neighbour_setter_sets(self):
        sut = Cell(None, None, CellType.worm)
        neighbour = Cell(None, None, CellType.food)
        sut.set_neighbour(Direction.right, neighbour)
        self.assertEqual(neighbour, sut.get_neighbour(Direction.right))
