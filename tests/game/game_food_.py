from src.game.global_refs import CellType
from tests.game.game_ import Game_


class Game_food_(Game_):
    def test_give_food_affects_one_cell(self):
        self.sut._last_food.be_blank()
        self.sut._give_food()
        expected = 1
        self.assertCellCount(self.sut._grid, CellType.food, expected)

    def test_give_food_initially_doesnt_change_diff(self):
        self.assertIsNone(self.sut._diff.food)
