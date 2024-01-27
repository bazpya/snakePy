from src.game.snake import Snake
from src.game.Result import SnakeResult
from game_test.helper.cell_factory import CellFactory
from src.game_test.snake_ import Snake_


class Snake_events_(Snake_):
    # ======================  Blank  ======================

    def test_blank_emits_the_right_events(self):
        origin = CellFactory.make_chain("bb")
        sut = Snake(origin)
        sut._events = self._events
        sut.step()
        self.stepped_callback.assert_called()
        self.ate_callback.assert_not_called()
        self.died_callback.assert_not_called()

    def test_blank_passes_diff_to_stepped_event(self):
        cells = CellFactory.make_list("bb")
        CellFactory.link(cells)
        origin = cells[0]
        destination = cells[1]
        sut = Snake(origin)
        sut._events = self._events
        sut.step()
        self.stepped_callback.assert_called_with([origin, destination])

    # # ======================  Food  ======================

    def test_food_emits_the_right_events(self):
        origin = CellFactory.make_chain("bf")
        sut = Snake(origin)
        sut._events = self._events
        sut.step()
        self.stepped_callback.assert_called()
        self.ate_callback.assert_called()
        self.died_callback.assert_not_called()

    def test_food_passes_diff_to_stepped_event(self):
        cells = CellFactory.make_list("bf")
        CellFactory.link(cells)
        origin = cells[0]
        destination = cells[1]
        sut = Snake(origin)
        sut._events = self._events
        sut.step()
        self.stepped_callback.assert_called_with([destination])

    # # ======================  Death  ======================

    def test_death_emits_the_right_events(self):
        origin = CellFactory.make_chain("bs")
        sut = Snake(origin)
        sut._events = self._events
        sut.step()
        self.stepped_callback.assert_called()
        self.ate_callback.assert_not_called()
        self.died_callback.assert_called()

    def test_death_passes_no_cells_to_stepped_event(self):
        cells = CellFactory.make_list("bw")
        CellFactory.link(cells)
        origin = cells[0]
        sut = Snake(origin)
        sut._events = self._events
        sut.step()
        self.stepped_callback.assert_called_with([])

    def test_death_passes_correct_result_to_died_event_single_cell(self):
        origin = CellFactory.make_chain("bw")
        sut = Snake(origin)
        sut._events = self._events
        sut.step()
        result: SnakeResult = self.died_callback.call_args[0][0]
        self.assertEqual(result.length, 1)
        self.assertEqual(result.steps_taken, 1)

    def test_death_passes_correct_result_to_died_event_multi_cell(self):
        pattern = "bbffbbs"
        origin = CellFactory.make_chain(pattern)
        sut = Snake(origin)
        sut._events = self._events
        for i in range(0, len(pattern) - 1):
            sut.step()
        result: SnakeResult = self.died_callback.call_args[0][0]
        self.assertEqual(result.length, 3)
        self.assertEqual(result.steps_taken, len(pattern) - 1)

    # ======================  ?????  ======================
