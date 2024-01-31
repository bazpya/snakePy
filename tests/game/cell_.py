import math
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
        for setter, type in (
            (Cell.be_blank, CellType.blank),
            (Cell.be_food, CellType.food),
            (Cell.be_snake, CellType.snake),
            (Cell.be_wall, CellType.wall),
        ):
            eval("sut." + setter.__name__ + "()")
            self.assertEqual(sut.type, type)

    def test_type_getters(self):
        for getter, type in (
            (Cell.is_blank, CellType.blank),
            (Cell.is_food, CellType.food),
            (Cell.is_snake, CellType.snake),
            (Cell.is_wall, CellType.wall),
        ):
            sut = Cell(None, None, type)
            self.assertTrue(eval("sut." + getter.__name__ + "()"))

    # ====================  Distances  ====================

    def test_get_distance_vertical(self):
        sut = Cell(self.few, self.many)
        target = Cell(self.some, self.many)
        res = sut.get_distance(target)
        expected = self.some - self.few
        self.assertEqual(res, (expected, 0, expected))

    def test_get_distance_horizontal(self):
        sut = Cell(self.many, self.few)
        target = Cell(self.many, self.some)
        res = sut.get_distance(target)
        expected = self.some - self.few
        self.assertEqual(res, (0, expected, expected))

    def test_get_distance_diagonal(self):
        sut = Cell(self.many, self.few)
        target = Cell(self.some, self.many)
        res = sut.get_distance(target)
        expected = (
            self.some - self.many,
            self.many - self.few,
            math.sqrt((self.some - self.many) ** 2 + (self.many - self.few) ** 2),
        )
        self.assertEqual(res, expected)

    # ====================  Reciprocal Distances  ====================

    def test_get_distance_vertical_reciprocal(self):
        sut = Cell(self.few, self.many)
        target = Cell(self.some, self.many)
        res = sut.get_distance(target, True)
        expected = 1 / (self.some - self.few)
        self.assertEqual(res, (expected, 0, abs(expected)))

    def test_get_distance_horizontal_reciprocal(self):
        sut = Cell(self.many, self.few)
        target = Cell(self.many, self.some)
        res = sut.get_distance(target, True)
        expected = 1 / (self.some - self.few)
        self.assertEqual(res, (0, expected, abs(expected)))

    def test_get_distance_diagonal_reciprocal(self):
        sut = Cell(self.many, self.few)
        target = Cell(self.some, self.many)
        res = sut.get_distance(target, True)
        expected = (
            1 / (self.some - self.many),
            1 / (self.many - self.few),
            1 / math.sqrt((self.some - self.many) ** 2 + (self.many - self.few) ** 2),
        )
        self.assertEqual(res, expected)
