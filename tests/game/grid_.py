from src.game.direction import Direction
from src.game.grid import Grid
from tests.test_ import Test_
from src.game.cell import Cell
from src.game.global_refs import CellType
from src.game.game import Game


class Grid_(Test_):
    def setUp(self):
        self.sut = Grid(self.few, self.some)

    def assertCellCount(self, game: Game, cell_type: CellType, expected: int):
        def counter_func(cell: Cell, ri, ci, acc):
            return acc + 1 if cell.type == cell_type else acc

        actual = game.iterate_cells(False, counter_func, 0)
        self.assertEqual(actual, expected)

    # ===========================  Init  ===========================

    def test_init_creates_correct_dimensions(self):
        self.assertEqual(self.few, len(self.sut._cells))
        for row in self.sut._cells:
            self.assertEqual(self.some, len(row))

    def test_init_with_one_dimension_creates_square(self):
        sut = Grid(self.few)
        self.assertEqual(self.few, sut.col_count)

    def test_init_creates_cell_instances(self):
        self.sut.iterate_cells(True, lambda *args: self.assertIsInstance(args[0], Cell))

    # ===========================  Areas  ===========================

    def test_horizontal_walls(self):
        first_row = self.sut._cells[0]
        last_row = self.sut._cells[-1]
        for cell in [*first_row, *last_row]:
            self.assertTrue(cell.is_wall())

    def test_vertical_walls(self):
        for r in range(self.few):
            first = self.sut._cells[r][0]
            last = self.sut._cells[r][-1]
            self.assertTrue(last.is_wall())
            self.assertTrue(first.is_wall())

    # ===========================  Neighbours  ===========================

    def test_middle_cells_have_all_neighbours(self):
        def visit(cell: Cell, ri, ci, acc):
            for dir in Direction:
                self.assertIsNotNone(cell.get_neighbour(dir))

        self.sut.iterate_cells(False, visit)

    def test_first_row_neighbours(self):
        first_row = self.sut._cells[0]
        for cell in first_row:
            self.assertIsNone(cell.get_neighbour(Direction.up))
            self.assertIsInstance(cell.get_neighbour(Direction.down), Cell)

    def test_last_row_neighbours(self):
        last_row = self.sut._cells[-1]
        for cell in last_row:
            self.assertIsInstance(cell.get_neighbour(Direction.up), Cell)
            self.assertIsNone(cell.get_neighbour(Direction.down))

    def test_first_col_neighbours(self):
        for r in range(self.few):
            cell = self.sut._cells[r][0]
            self.assertIsNone(cell.get_neighbour(Direction.left))
            self.assertIsInstance(cell.get_neighbour(Direction.right), Cell)

    def test_last_col_neighbours(self):
        for r in range(self.few):
            cell = self.sut._cells[r][-1]
            self.assertIsInstance(cell.get_neighbour(Direction.left), Cell)
            self.assertIsNone(cell.get_neighbour(Direction.right))

    # ===========================  Iterate  ===========================

    def test_iterate_cells_hits_all_cells(self):
        expected = self.few * self.some
        actual = self.sut.iterate_cells(True, lambda *args: args[-1] + 1, 0)
        self.assertEqual(actual, expected)

    def test_iterate_cells_hits_interior_cells(self):
        expected = (self.few - 2) * (self.some - 2)
        actual = self.sut.iterate_cells(False, lambda *args: args[-1] + 1, 0)
        self.assertEqual(expected, actual)

    # ===========================  Centre  ===========================

    def test_get_centre_for_large_numbers(self):
        expected = self.some
        sut = Grid(expected * 2 + 1)  # odd
        actual = sut._get_centre()._row
        self.assertEqual(expected, actual)
        sut = Grid(expected * 2)  # even
        actual = sut._get_centre()._row
        self.assertEqual(expected, actual)

    def test_get_centre_for_small_numbers(self):
        expected = 2
        sut = Grid(expected * 2 + 1)  # odd
        actual = sut._get_centre()._row
        self.assertEqual(expected, actual)
        sut = Grid(4)  # even
        actual = sut._get_centre()._row
        self.assertEqual(expected, actual)

    # ===========================  Cell Getters  ===========================

    def test_get_blank_cells_gets_blanks(self):
        for cell in self.sut._get_blanks():
            self.assertTrue(cell.is_blank())

    def test_get_blank_cells_gets_correct_number_of_cells(self):
        expected = (self.few - 2) * (self.some - 2)
        res = self.sut._get_blanks()
        actual = len(res)
        self.assertEqual(actual, expected)

    def test_get_flat_gets_correct_number_of_cells(self):
        expected = self.few * self.some
        actual = len(self.sut.get_flat())
        self.assertEqual(actual, expected)
