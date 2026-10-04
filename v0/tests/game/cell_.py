import math
from tests.game.helper.cell_factory import CellFactory
from tests.testbase import Test_
from src.game.cell import CellType, Cell
from src.game.direction import Direction


class Cell_(Test_):

    def __init__(self, methodName: str = "runTest") -> None:
        self.sut = Cell()
        super().__init__(methodName)

    def test_init_with_unspecified_type_defaults_to_blank(self):
        expected = CellType.blank
        actual = self.sut.type
        self.assertEqual(actual, expected)

    def test_init_with_specified_type_sets_type(self):
        for expected in list(CellType):
            with self.subTest():
                sut = Cell(None, None, expected)
                actual = sut.type
                self.assertEqual(actual, expected)

    def test_init_sets_neighbours_to_none(self):
        for dir in list(Direction):
            with self.subTest():
                self.assertIsNone(self.sut.get_neighbour(dir))

    def test_neighbour_setter_sets(self):
        for type in list(CellType):
            for dir in list(Direction):
                with self.subTest():
                    expected = Cell(None, None, type)
                    self.sut.set_neighbour(dir, expected)
                    actual = self.sut.get_neighbour(dir)
                    self.assertEqual(actual, expected)

    def test_type_setters(self):
        for setter, expected in (
            (Cell.be_blank, CellType.blank),
            (Cell.be_food, CellType.food),
            (Cell.be_snake, CellType.snake),
            (Cell.be_wall, CellType.wall),
        ):
            with self.subTest():
                eval("self.sut." + setter.__name__ + "()")
                actual = self.sut.type
                self.assertEqual(actual, expected)

    def test_type_getters(self):
        for getter, expected in (
            (Cell.is_blank, CellType.blank),
            (Cell.is_food, CellType.food),
            (Cell.is_snake, CellType.snake),
            (Cell.is_wall, CellType.wall),
        ):
            with self.subTest():
                sut = Cell(None, None, expected)
                self.assertTrue(eval("sut." + getter.__name__ + "()"))

    # ====================  Distances  ====================

    def test_get_distance_vertical(self):
        sut = Cell(self.few, self.many)
        other = Cell(self.some, self.many)
        diff = other._row - sut._row
        actual = sut.get_distance(False, other)
        expected = (diff, 0, diff)
        self.assertEqual(actual, expected)
        diff = 1 / diff
        actual = sut.get_distance(True, other)
        expected = (diff, 0, abs(diff))
        self.assertEqual(actual, expected)

    def test_get_distance_horizontal(self):
        sut = Cell(self.many, self.few)
        other = Cell(self.many, self.some)
        diff = self.some - self.few
        actual = sut.get_distance(False, other)
        expected = (0, diff, diff)
        self.assertEqual(actual, expected)
        diff = 1 / diff
        actual = sut.get_distance(True, other)
        expected = (0, diff, abs(diff))
        self.assertEqual(actual, expected)

    def test_get_distance_diagonal(self):
        sut = Cell(self.many, self.few)
        other = Cell(self.some, self.many)
        diff_row = self.some - self.many
        diff_col = self.many - self.few
        expected = (diff_row, diff_col, math.sqrt(diff_row**2 + diff_col**2))
        actual = sut.get_distance(False, other)
        self.assertEqual(actual, expected)
        expected = (
            1 / (diff_row),
            1 / (diff_col),
            1 / math.sqrt(diff_row**2 + diff_col**2),
        )
        actual = sut.get_distance(True, other)
        self.assertEqual(actual, expected)

    # ====================  Death Distance  ====================

    def test_death_distance_to_self(self):
        sut = Cell(self.some, self.few, CellType.snake)
        expected = (0, 0, 0)
        actual = sut.death_distance(False, Direction.any())
        self.assertEqual(actual, expected)
        expected = (0, 0, 0)
        actual = sut.death_distance(True, Direction.any())
        self.assertEqual(actual, expected)

    def test_death_distance_to_neighbour(self):
        sut = Cell(self.some, self.few)
        other = Cell(sut._row + 1, sut._col - 1, CellType.snake)
        sut.get_neighbour = CellFactory._make_getter(other)
        actual = sut.death_distance(False, Direction.any())
        expected = (1, -1, math.sqrt(2))
        self.assertEqual(actual, expected)
        actual = sut.death_distance(True, Direction.any())
        expected = (1, -1, 1 / math.sqrt(2))
        self.assertEqual(actual, expected)
