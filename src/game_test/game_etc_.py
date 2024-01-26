from src.game.global_refs import CellType
from src.game.game import Game
from src.game.cell import Cell
from src.game_test.game_ import Game_


class Game_etc_(Game_):
    def test_iterate_cells_hits_all_cells(self):
        all_cells_count = self.row_count * self.col_count

        def counter_func(cell: Cell, ri, ci, acc):
            return acc + 1

        count = self._sut.iterate_cells(True, counter_func, 0)
        self.assertEqual(all_cells_count, count)

    def test_iterate_cells_hits_interior_cells(self):
        interior_cells_count = (self.row_count - 2) * (self.col_count - 2)

        def counter_func(cell: Cell, ri, ci, acc):
            return acc + 1

        count = self._sut.iterate_cells(False, counter_func, 0)
        self.assertEqual(interior_cells_count, count)

    def test_get_blank_cells_gets_blanks(self):
        actual = self._sut._get_blank_cells()
        for cell in actual:
            self.assertTrue(cell.is_blank())

    def test_get_blank_cells_gets_correct_number_of_cells(self):
        supposed_blanks = self._sut._get_blank_cells()
        actual = len(supposed_blanks)
        expected = (
            (self.row_count - 2) * (self.col_count - 2) - self._sut._ini_food_count - 1
        )
        self.assertEqual(actual, expected)

    def test_get_centre_for_large_odd_numbers(self):
        expected = 8
        sut = Game(expected * 2 + 1)
        cell = sut._get_centre()
        actual = cell._row
        self.assertEqual(expected, actual)

    def test_get_centre_for_large_even_numbers(self):
        expected = 8
        sut = Game(expected * 2)
        cell = sut._get_centre()
        actual = cell._row
        self.assertEqual(expected, actual)

    def test_get_centre_for_small_odd_numbers(self):
        expected = 2
        sut = Game(expected * 2 + 1)
        cell = sut._get_centre()
        actual = cell._row
        self.assertEqual(expected, actual)

    def test_get_centre_for_small_even_numbers(self):
        expected = 2
        sut = Game(4)
        cell = sut._get_centre()
        actual = cell._row
        self.assertEqual(expected, actual)

    def test_add_snake_sets_one_cell(self):
        self.assertCellCount(self._sut, CellType.snake, 1)
