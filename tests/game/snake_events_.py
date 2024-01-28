from src.game.Diff import SnakeDiff
from src.game.snake import Snake
from src.game.Result import SnakeResult
from tests.game.helper.cell_factory import CellFactory
from tests.game.snake_ import Snake_sync_


class Snake_events_(Snake_sync_):
    # ======================  Blank  ======================

    def test_blank_emits_the_right_events(self):
        origin = CellFactory.make_chain("bb")
        sut = Snake(origin)
        sut._events = self._events
        sut.step()
        self.stepped_callback.assert_called_once()
        self.ate_callback.assert_not_called()
        self.died_callback.assert_not_called()

    def test_blank_passes_diff_to_stepped_event(self):
        cells = CellFactory.make_list("bb")
        CellFactory.link(cells)
        origin = cells[0]
        next = cells[1]
        sut = Snake(origin)
        sut._events = self._events
        sut.step()
        diff: SnakeDiff = self.stepped_callback.call_args[0][0]
        self.assertListEqual(diff.blanks, [origin])
        self.assertListEqual(diff.snakes, [next])

    # ======================  Food  ======================

    def test_food_emits_the_right_events(self):
        origin = CellFactory.make_chain("bf")
        sut = Snake(origin)
        sut._events = self._events
        sut.step()
        self.stepped_callback.assert_called_once()
        self.ate_callback.assert_called_once()
        self.died_callback.assert_not_called()

    def test_food_passes_diff_to_stepped_event(self):
        cells = CellFactory.make_list("bf")
        CellFactory.link(cells)
        origin = cells[0]
        next = cells[1]
        sut = Snake(origin)
        sut._events = self._events
        sut.step()
        self.stepped_callback.assert_called_once()
        diff: SnakeDiff = self.stepped_callback.call_args[0][0]
        self.assertListEqual(diff.snakes, [next])

    # ======================  Death  ======================

    def test_death_emits_the_right_events(self):
        origin = CellFactory.make_chain("bs")
        sut = Snake(origin)
        sut._events = self._events
        sut.step()
        self.stepped_callback.assert_called_once()
        self.ate_callback.assert_not_called()
        self.died_callback.assert_called_once()

    def test_death_passes_no_cells_to_stepped_event(self):
        cells = CellFactory.make_list("bw")
        CellFactory.link(cells)
        origin = cells[0]
        sut = Snake(origin)
        sut._events = self._events
        sut.step()
        self.stepped_callback.assert_called_once()
        diff: SnakeDiff = self.stepped_callback.call_args[0][0]
        self.assertListEmpty(diff.blanks)
        self.assertListEmpty(diff.snakes)
