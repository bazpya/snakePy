from src.game.snake import Snake
from src.game.game import Game
from tests.game.game_ import Game_
from tests.game.helper.counter import Counter
from tests.game.helper.cell_factory import CellFactory


class Game_events_(Game_):
    # ======================  Blank  ======================

    def test_blank_emits_the_right_events(self):
        origin = CellFactory.make_chain("bb")
        snake = Snake(origin)
        self._sut._bind(snake)
        snake.step()
        self.stepped_callback.assert_called_once()
        self.ate_callback.assert_not_called()
        self.died_callback.assert_not_called()
        self.ready_to_draw_callback.assert_called_once()

    def test_blank_passes_diff_to_stepped_event(self):
        cells = CellFactory.make_list("bb")
        CellFactory.link(cells)
        origin = cells[0]
        snake = Snake(origin)
        self._sut._bind(snake)
        snake.step()
        diff = self.stepped_callback.call_args[0][0]
        self.assertEqual(set(diff), set(cells))  # for unordered comparison

    # # ======================  Food  ======================

    def test_food_emits_the_right_events(self):
        origin = CellFactory.make_chain("bf")
        snake = Snake(origin)
        self._sut._bind(snake)
        snake.step()
        self.stepped_callback.assert_called_once()
        self.ate_callback.assert_called_once()
        self.died_callback.assert_not_called()
        self.ready_to_draw_callback.assert_called_once()

    def test_food_passes_diff_to_stepped_event(self):
        cells = CellFactory.make_list("bf")
        CellFactory.link(cells)
        origin = cells[0]
        next = cells[1]
        snake = Snake(origin)
        self._sut._bind(snake)
        snake.step()
        self.stepped_callback.assert_called_once_with([next])

    # # ======================  Death  ======================

    def test_death_emits_the_right_events(self):
        origin = CellFactory.make_chain("bs")
        snake = Snake(origin)
        self._sut._bind(snake)
        snake.step()
        self.stepped_callback.assert_called_once()
        self.ate_callback.assert_not_called()
        self.died_callback.assert_called_once()
        self.ready_to_draw_callback.assert_called_once()

    def test_death_passes_no_cells_to_stepped_event(self):
        origin = CellFactory.make_chain("bw")
        snake = Snake(origin)
        self._sut._bind(snake)
        snake.step()
        self.stepped_callback.assert_called_once_with([])

    def test_run_sync_at_specified_number_of_steps_emits_died_event(self):
        counter = Counter()
        sut = Game(self.row_count, self.col_count, steps_to_take=self.few)
        sut.events = self._events
        sut.events.stepped.subscribe(counter.increment)
        sut.run_sync()
        self.died_callback.assert_called_once()
        self.assertEqual(counter.read(), self.few)
