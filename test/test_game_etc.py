from source.game import Game
from source.cell import Cell
from test.test_game_ import Game_


class Game_etc_(Game_):
    def test_iterate_cells_hits_all_cells(self):
        all_cells_count = self.row_count * self.col_count

        def counter_func(cell: Cell, ri, ci, acc):
            return acc + 1

        sut = self.make_sut()
        count = sut.iterate_cells(True, counter_func, 0)
        self.assertEqual(all_cells_count, count)

    def test_iterate_cells_hits_interior_cells(self):
        interior_cells_count = (self.row_count - 2) * (self.col_count - 2)

        def counter_func(cell: Cell, ri, ci, acc):
            return acc + 1

        sut = self.make_sut()
        count = sut.iterate_cells(False, counter_func, 0)
        self.assertEqual(interior_cells_count, count)

    def test_get_blank_cells_gets_blanks(self):
        sut = self.make_sut()
        actual = sut._get_blank_cells()
        for cell in actual:
            self.assertTrue(cell.is_blank())

    def test_get_blank_cells_gets_correct_number_of_cells(self):
        sut = self.make_sut()
        supposed_blanks = sut._get_blank_cells()
        count = len(supposed_blanks)
        self.assertEqual((self.row_count - 2) * (self.col_count - 2), count)

    def test_add_food_without_args_affects_one_cell(self):
        sut = self.make_sut()
        food_cell = sut._add_food()

        def counter_func(cell: Cell, ri, ci, acc):
            return acc + 1 if cell.is_food() else acc

        count = sut.iterate_cells(False, counter_func, 0)
        self.assertEqual(1, count)

    def test_add_food_with_specific_number_adds_correct_amount(self):
        sut = self.make_sut()
        food_cell = sut._add_food(self._some_number_1)

        def counter_func(cell: Cell, ri, ci, acc):
            return acc + 1 if cell.is_food() else acc

        count = sut.iterate_cells(False, counter_func, 0)
        self.assertEqual(count, self._some_number_1)

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
        expected = 1
        sut = Game(expected * 2 + 1)
        cell = sut._get_centre()
        actual = cell._row
        self.assertEqual(expected, actual)

    def test_get_centre_for_small_even_numbers(self):
        expected = 1
        sut = Game(expected * 2)
        cell = sut._get_centre()
        actual = cell._row
        self.assertEqual(expected, actual)

    def test_add_snake_sets_one_cell(self):
        sut = self.make_sut()

        def counter_func(cell: Cell, ri, ci, acc):
            return acc + 1 if cell.is_snake() else acc

        sut.add_snake()
        count = sut.iterate_cells(True, counter_func, 0)
        self.assertEqual(1, count)
