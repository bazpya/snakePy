from source.cell import CellType, Cell
from source.global_refs import Direction
from test.test_cell_ import Cell_


class Cell_types_(Cell_):
    def test_getter_and_attribute_return_same(self):
        expected = CellType.snake
        sut = Cell(None, None, expected)
        self.assertEqual(sut.get_type(), sut._type)

    def test_be_wall_makes_wall(self):
        sut = Cell(None, None)
        sut.be_wall()
        self.assertEqual(CellType.wall, sut.get_type())

    def test_be_snake_makes_snake(self):
        sut = Cell(None, None)
        sut.be_snake()
        self.assertEqual(CellType.snake, sut.get_type())

    def test_be_food_makes_food(self):
        sut = Cell(None, None)
        sut.be_food()
        self.assertEqual(CellType.food, sut.get_type())

    def test_be_blank_makes_blank(self):
        sut = Cell(None, None, CellType.food)
        sut.be_blank()
        self.assertEqual(CellType.blank, sut.get_type())

    def test_is_snake_works(self):
        sut = Cell(None, None, CellType.snake)
        self.assertTrue(sut.is_snake())
