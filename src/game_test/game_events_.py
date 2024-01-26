from src.game.snake import Snake
from src.game.Result import GameResult
from src.game_test.game_ import Game_
from src.game_test.helper.path_factory import PathFactory


class Game_events_(Game_):
    # ======================  Blank  ======================

    def test_blank_step_emits_the_right_events(self):
        sut = self.make_sut()
        sut._events = self._events
        origin = PathFactory.make_chain("bb")
        snake = Snake(origin)
        sut._bind(snake)
        snake.step()
        self.stepped_callback.assert_called()
        self.ate_callback.assert_not_called()
        self.died_callback.assert_not_called()
        self.ready_to_draw_callback.assert_called()

    def test_blank_step_passes_diff_to_stepped_event(self):
        sut = self.make_sut()
        sut._events = self._events
        cells = PathFactory.make_list("bb")
        PathFactory.link(cells)
        origin = cells[0]
        next = cells[1]
        snake = Snake(origin)
        sut._bind(snake)
        snake.step()
        self.stepped_callback.assert_called_with([origin, next])

    # # ======================  Food  ======================

    def test_food_step_emits_the_right_events(self):
        sut = self.make_sut()
        sut._events = self._events
        origin = PathFactory.make_chain("bf")
        snake = Snake(origin)
        sut._bind(snake)
        snake.step()
        self.stepped_callback.assert_called()
        self.ate_callback.assert_called()
        self.died_callback.assert_not_called()
        self.ready_to_draw_callback.assert_called()

    def test_food_step_passes_diff_to_stepped_event(self):
        sut = self.make_sut()
        sut._events = self._events
        cells = PathFactory.make_list("bf")
        PathFactory.link(cells)
        origin = cells[0]
        next = cells[1]
        snake = Snake(origin)
        sut._bind(snake)
        snake.step()
        self.stepped_callback.assert_called_with([next])

    # # ======================  Death  ======================

    def test_death_step_emits_the_right_events(self):
        sut = self.make_sut()
        sut._events = self._events
        origin = PathFactory.make_chain("bs")
        snake = Snake(origin)
        sut._bind(snake)
        snake.step()
        self.stepped_callback.assert_called()
        self.ate_callback.assert_not_called()
        self.died_callback.assert_called()
        self.ready_to_draw_callback.assert_called()

    def test_death_step_passes_no_cells_to_stepped_event(self):
        sut = self.make_sut()
        sut._events = self._events
        origin = PathFactory.make_chain("bw")
        snake = Snake(origin)
        sut._bind(snake)
        snake.step()
        self.stepped_callback.assert_called_with([])

    def test_death_step_passes_correct_result_to_died_event_single_cell(self):
        sut = self.make_sut()
        sut._events = self._events
        origin = PathFactory.make_chain("bw")
        snake = Snake(origin)
        sut._bind(snake)
        snake.step()
        result: GameResult = self.died_callback.call_args[0][0]
        self.assertEqual(result.length, 1)
        self.assertEqual(result.steps_taken, 1)

    def test_death_step_passes_correct_result_to_died_event_multi_cell(self):
        sut = self.make_sut()
        sut._events = self._events
        path_pattern = "bbffbbs"
        origin = PathFactory.make_chain(path_pattern)
        snake = Snake(origin)
        sut._bind(snake)
        for i in range(0, len(path_pattern) - 1):
            snake.step()

        result: GameResult = self.died_callback.call_args[0][0]
        self.assertEqual(result.length, 3)
        self.assertEqual(result.steps_taken, len(path_pattern) - 1)

    def test_death_step_passes_foods_taken_to_died_event(self):
        self.skipTest("todo")

    def test_death_step_passes_turs_taken_to_died_event(self):
        self.skipTest("todo")
