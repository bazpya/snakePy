from tests.test_ import Test_
from src.game.cell import CellType, Cell
from src.game.direction import Direction


class Cell_(Test_):
    def test_init_with_unspecified_type_defaults_to_blank(self):
        expected = CellType.blank
        sut = Cell()
        self.assertEqual(sut.type, expected)

    def test_init_with_specified_type_sets_type(self):
        expected = CellType.wall
        sut = Cell(None, None, expected)
        self.assertEqual(sut.type, expected)

    def test_init_sets_neighbours_to_none(self):
        sut = Cell()
        for dir in list(Direction):
            self.assertIsNone(sut.get_neighbour(dir))

    def test_neighbour_setter_sets(self):
        sut = Cell(None, None, CellType.snake)
        for type in list(CellType):
            for dir in list(Direction):
                neighbour = Cell(None, None, type)
                sut.set_neighbour(dir, neighbour)
                self.assertEqual(sut.get_neighbour(dir), neighbour)

    def test_type_setters(self):
        sut = Cell()
        sut.be_wall()
        self.assertEqual(sut.type, CellType.wall)
        sut.be_snake()
        self.assertEqual(sut.type, CellType.snake)
        sut.be_food()
        self.assertEqual(sut.type, CellType.food)
        sut.be_blank()
        self.assertEqual(sut.type, CellType.blank)

    def test_type_getters(self):
        sut = Cell(None, None, CellType.blank)
        self.assertTrue(sut.is_blank())
        sut = Cell(None, None, CellType.food)
        self.assertTrue(sut.is_food())
        sut = Cell(None, None, CellType.snake)
        self.assertTrue(sut.is_snake())
        sut = Cell(None, None, CellType.wall)
        self.assertTrue(sut.is_wall())
