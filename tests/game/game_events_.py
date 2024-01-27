from src.game.snake import Snake
from src.game.Result import GameResult
from tests.game.game_ import Game_
from tests.game.helper.cell_factory import CellFactory


class Game_events_(Game_):
    # ======================  Blank  ======================

    def test_blank_step_emits_the_right_events(self):
        origin = CellFactory.make_chain("bb")
        snake = Snake(origin)
        self._sut._bind(snake)
        snake.step()
        self.stepped_callback.assert_called_once()
        self.ate_callback.assert_not_called()
        self.died_callback.assert_not_called()
        self.ready_to_draw_callback.assert_called_once()

    def test_blank_step_passes_diff_to_stepped_event(self):
        cells = CellFactory.make_list("bb")
        CellFactory.link(cells)
        origin = cells[0]
        snake = Snake(origin)
        self._sut._bind(snake)
        snake.step()
        diff = self.stepped_callback.call_args[0][0]
        self.assertEqual(set(diff), set(cells))  # for unordered comparison

    # # ======================  Food  ======================

    def test_food_step_emits_the_right_events(self):
        origin = CellFactory.make_chain("bf")
        snake = Snake(origin)
        self._sut._bind(snake)
        snake.step()
        self.stepped_callback.assert_called_once()
        self.ate_callback.assert_called_once()
        self.died_callback.assert_not_called()
        self.ready_to_draw_callback.assert_called_once()

    def test_food_step_passes_diff_to_stepped_event(self):
        cells = CellFactory.make_list("bf")
        CellFactory.link(cells)
        origin = cells[0]
        next = cells[1]
        snake = Snake(origin)
        self._sut._bind(snake)
        snake.step()
        self.stepped_callback.assert_called_once_with([next])

    # # ======================  Death  ======================

    def test_death_step_emits_the_right_events(self):
        origin = CellFactory.make_chain("bs")
        snake = Snake(origin)
        self._sut._bind(snake)
        snake.step()
        self.stepped_callback.assert_called_once()
        self.ate_callback.assert_not_called()
        self.died_callback.assert_called_once()
        self.ready_to_draw_callback.assert_called_once()

    def test_death_step_passes_no_cells_to_stepped_event(self):
        origin = CellFactory.make_chain("bw")
        snake = Snake(origin)
        self._sut._bind(snake)
        snake.step()
        self.stepped_callback.assert_called_once_with([])

    def test_death_step_passes_correct_result_to_died_event_single_cell(self):
        origin = CellFactory.make_chain("bw")
        snake = Snake(origin)
        self._sut._bind(snake)
        snake.step()
        result: GameResult = self.died_callback.call_args[0][0]
        self.assertEqual(result.length, 1)
        self.assertEqual(result.steps_taken, 1)

    def test_death_step_passes_correct_result_to_died_event_multi_cell(self):
        pattern = "bbffbbs"
        origin = CellFactory.make_chain(pattern)
        snake = Snake(origin)
        self._sut._bind(snake)
        for i in range(0, len(pattern) - 1):  # todo: replace with run(5)
            snake.step()

        result: GameResult = self.died_callback.call_args[0][0]
        self.assertEqual(result.length, 3)
        self.assertEqual(result.steps_taken, len(pattern) - 1)

    # todo:
    # def test_death_step_passes_turs_taken_to_died_event(self):
    #     turns = [Turn.left, Turn.right, Turn.ahead, Turn.ahead, Turn.right]
    #     for turn in turns:
    #         self._sut.turn(turn)
    #     self._sut.run_sync(2)
    #     self.died_callback.assert_called_once()
    #     # result: GameResult = self.died_callback.call_args[0][0]
    #     # self.assertEqual(result.turns, turns)

    def test_death_step_passes_foods_taken_to_died_event(self):
        self.skipTest("todo")
