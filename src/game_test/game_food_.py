from src.game.global_refs import CellType
from src.game.cell import Cell
from src.game.game import Game
from src.game_test.game_ import Game_


class Game_etc_(Game_):
    def test_add_food_without_args_affects_one_cell(self):
        food_cell = self._sut._add_food()
        expected = self._sut._ini_food_count + 1
        self.assertCellCount(self._sut, CellType.food, expected)

    def test_add_food_with_specific_number_adds_correct_amount(self):
        food_cell = self._sut._add_food(self._some_number_1)
        expected = self._some_number_1 + self._sut._ini_food_count
        self.assertCellCount(self._sut, CellType.food, expected)

    def test_initiates_correct_number_of_foods(self):
        expected = self._some_number_1
        sut = Game(self._some_number_2, init_food_count=expected)
        self.assertCellCount(sut, CellType.food, expected)
