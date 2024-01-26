from src.game.snake import Snake
from src.game.Result import SnakeResult
from src.game_test.helper.path_factory import PathFactory
from src.game_test.snake_ import Snake_


class Snake_events_(Snake_):
    # ======================  Blank  ======================

    def test_blank_emits_the_right_events(self):
        origin = PathFactory.make_chain("bb")
        sut = Snake(origin)
        sut._events = self._events
        sut.step()
        self.stepped_callback.assert_called()
        self.ate_callback.assert_not_called()
        self.died_callback.assert_not_called()

    def test_blank_passes_diff_to_stepped_event(self):
        cells = PathFactory.make_list("bb")
        PathFactory.link(cells)
        origin = cells[0]
        destination = cells[1]
        sut = Snake(origin)
        sut._events = self._events
        sut.step()
        self.stepped_callback.assert_called_with([origin, destination])

    # # ======================  Food  ======================

    def test_food_emits_the_right_events(self):
        origin = PathFactory.make_chain("bf")
        sut = Snake(origin)
        sut._events = self._events
        sut.step()
        self.stepped_callback.assert_called()
        self.ate_callback.assert_called()
        self.died_callback.assert_not_called()

    def test_food_passes_diff_to_stepped_event(self):
        cells = PathFactory.make_list("bf")
        PathFactory.link(cells)
        origin = cells[0]
        destination = cells[1]
        sut = Snake(origin)
        sut._events = self._events
        sut.step()
        self.stepped_callback.assert_called_with([destination])

    # # ======================  Death  ======================

    def test_death_emits_the_right_events(self):
        origin = PathFactory.make_chain("bs")
        sut = Snake(origin)
        sut._events = self._events
        sut.step()
        self.stepped_callback.assert_called()
        self.ate_callback.assert_not_called()
        self.died_callback.assert_called()

    def test_death_passes_no_cells_to_stepped_event(self):
        cells = PathFactory.make_list("bw")
        PathFactory.link(cells)
        origin = cells[0]
        sut = Snake(origin)
        sut._events = self._events
        sut.step()
        self.stepped_callback.assert_called_with([])

    def test_death_passes_correct_result_to_died_event_single_cell(self):
        origin = PathFactory.make_chain("bw")
        sut = Snake(origin)
        sut._events = self._events
        sut.step()
        result: SnakeResult = self.died_callback.call_args[0][0]
        self.assertEqual(result.length, 1)
        self.assertEqual(result.steps_taken, 1)

    def test_death_passes_correct_result_to_died_event_multi_cell(self):
        path_pattern = "bbffbbs"
        origin = PathFactory.make_chain(path_pattern)
        sut = Snake(origin)
        sut._events = self._events
        for i in range(0, len(path_pattern) - 1):
            sut.step()
        result: SnakeResult = self.died_callback.call_args[0][0]
        self.assertEqual(result.length, 3)
        self.assertEqual(result.steps_taken, len(path_pattern) - 1)

    # ======================  ?????  ======================
