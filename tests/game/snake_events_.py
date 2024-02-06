from src.game.diff import SnakeDiff
from src.game.snake import Snake
from tests.game.helper.cell_factory import CellFactory
from tests.game.snake_ import Snake_sync_


class Snake_events_(Snake_sync_):
    # ======================  Blank  ======================

    def test_blank_emits_the_right_events(self):
        origin, *etc = CellFactory.make("bb")
        sut = Snake(origin)
        sut._events = self._events
        sut.step()
        self.stepped_callback.assert_called_once()
        self.ate_callback.assert_not_called()
        self.died_callback.assert_not_called()

    def test_blank_passes_diff_to_stepped_event(self):
        origin, cells = CellFactory.make("bb")
        next = cells[1]
        sut = Snake(origin)
        sut._events = self._events
        sut.step()
        diff: SnakeDiff = self.stepped_callback.call_args[0][0]
        self.assertEqual(diff.blank, origin)
        self.assertEqual(diff.snake, next)

    # ======================  Food  ======================

    def test_food_emits_the_right_events(self):
        origin, *etc = CellFactory.make("bf")
        sut = Snake(origin)
        sut._events = self._events
        sut.step()
        self.stepped_callback.assert_called_once()
        self.ate_callback.assert_called_once()
        self.died_callback.assert_not_called()

    def test_food_passes_diff_to_stepped_event(self):
        origin, cells = CellFactory.make("bf")
        next = cells[1]
        sut = Snake(origin)
        sut._events = self._events
        sut.step()
        self.stepped_callback.assert_called_once()
        diff: SnakeDiff = self.stepped_callback.call_args[0][0]
        self.assertEqual(diff.snake, next)

    # ======================  Death  ======================

    def test_death_emits_the_right_events(self):
        origin, *etc = CellFactory.make("bs")
        sut = Snake(origin)
        sut._events = self._events
        sut.step()
        self.stepped_callback.assert_called_once()
        self.ate_callback.assert_not_called()
        self.died_callback.assert_called_once()

    def test_death_passes_no_cells_to_stepped_event(self):
        origin, *etc = CellFactory.make("bw")
        sut = Snake(origin)
        sut._events = self._events
        sut.step()
        self.stepped_callback.assert_called_once()
        diff: SnakeDiff = self.stepped_callback.call_args[0][0]
        self.assertIsNone(diff.blank)
        self.assertIsNone(diff.snake)
