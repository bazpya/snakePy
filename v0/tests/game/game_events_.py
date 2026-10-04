from src.game.global_refs import CauseOfDeath
from src.game.result import SnakeResult
from src.game.global_refs import CellType
from src.game.cell import Cell
from src.game.diff import GameDiff, SnakeDiff
from src.game.result import GameResult, SnakeResult
from tests.game.game_ import Game_


class Game_events_(Game_):
    # ======================  Blank  ======================

    def test_stepped_emits_the_right_events(self):
        self.sut._snake._events.stepped.emit(SnakeDiff())
        self.stepped_callback.assert_called_once()
        self.ate_callback.assert_not_called()
        self.died_callback.assert_not_called()

    def test_passes_snake_diff_to_stepped_event(self):
        b_cell, s_cell = Cell(CellType.blank), Cell(CellType.snake)
        snake_diff = SnakeDiff()
        snake_diff.set_blank(b_cell)
        snake_diff.set_snake(s_cell)
        self.sut._snake._events.stepped.emit(snake_diff)
        diff: GameDiff = self.stepped_callback.call_args[0][0]
        self.assertEqual(diff.blank, b_cell)
        self.assertEqual(diff.snake, s_cell)

    # ======================  Food  ======================

    def test_ate_emits_the_right_events(self):
        self.sut._snake._events.ate.emit()
        self.stepped_callback.assert_not_called()
        self.ate_callback.assert_called_once()
        self.died_callback.assert_not_called()

    def test_give_food_causes_diff_to_stepped_event(self):
        f_cell = Cell()
        self.sut._grid.get_random_blanks = self.make_getter([f_cell])
        self.sut._give_food()
        self.sut._snake._events.stepped.emit(SnakeDiff())
        diff: GameDiff = self.stepped_callback.call_args[0][0]
        self.assertEqual(diff.food, f_cell)

    # ======================  Death  ======================

    def test_death_emits_the_right_events(self):
        self.sut._snake._events.died.emit(SnakeResult(1, 2, None, 3))
        self.stepped_callback.assert_not_called()
        self.ate_callback.assert_not_called()
        self.died_callback.assert_called_once()

    def test_emits_died_event_with_wrapped_snake_result(self):
        snake_res = SnakeResult(self.many, self.some, CauseOfDeath.wall, self.few)
        self.sut._snake._events.died.emit(snake_res)
        result: GameResult = self.died_callback.call_args[0][0]
        self.assertEqual(result.snake, snake_res)
