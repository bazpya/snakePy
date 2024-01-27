from unittest.mock import MagicMock
from src.game.cell import Cell
from src.game.direction import Direction
from src.game.snake import Snake
from src.game.Result import SnakeResult
from src.game_test.helper.path_factory import PathFactory
from src.game_test.snake_ import Snake_


class Snake_step_(Snake_):
    # ===============================  step-blank  ===============================

    def test_step_into_blank_moves_head(self):
        cells = PathFactory.make_list("bb")
        PathFactory.link(cells)
        origin = cells[0]
        destination = cells[1]
        sut = Snake(origin)
        sut._events = self._events
        sut.step()
        self.assertEqual(destination, sut.get_head())

    def test_step_into_blank_makes_new_cell_snake(self):
        cells = PathFactory.make_list("bb")
        PathFactory.link(cells)
        origin = cells[0]
        destination = cells[1]
        sut = Snake(origin)
        sut._events = self._events
        sut.step()
        self.assertTrue(destination.is_snake())

    def test_step_into_blank_makes_tail_cell_blank(self):
        origin = PathFactory.make_chain("bb")
        sut = Snake(origin)
        sut._events = self._events
        sut.step()
        self.assertTrue(origin.is_blank())

    def test_step_into_blank_keeps_length_same(self):
        origin = PathFactory.make_chain("bb")
        sut = Snake(origin)
        sut._events = self._events
        initial_length = sut.get_length()
        sut.step()
        self.assertEqual(initial_length, sut.get_length())

    def test_step_into_blank_pops_from_steering(self):
        origin = Cell()
        sut = Snake(origin)
        origin.get_neighbour = MagicMock()
        dir = Direction.up
        sut.direction_enque(dir)
        sut.step()
        origin.get_neighbour.assert_called_once_with(dir)

    def test_step_into_blank_when_reached_step_count_dies(self):
        origin = PathFactory.make_infinite_chain()
        sut = Snake(origin, self._medium_number)
        sut._events = self._events
        sut.run_sync()
        result: SnakeResult = self.died_callback.call_args[0][0]
        self.assertEqual(result.steps_taken, self._medium_number)

    # ===============================  step-food  ===============================

    def test_step_into_food_increments_length(self):
        origin = PathFactory.make_chain("bf")
        sut = Snake(origin)
        sut._events = self._events
        initial_length = sut.get_length()
        sut.step()
        self.assertEqual(initial_length + 1, sut.get_length())

    def test_step_into_food_when_reached_step_count_dies(self):
        origin = PathFactory.make_chain("f" * (self._large_number))
        sut = Snake(origin, self._medium_number)
        sut._events = self._events
        sut.run_sync()
        result: SnakeResult = self.died_callback.call_args[0][0]
        self.assertEqual(result.steps_taken, self._medium_number)

    # ===============================  step-death  ===============================

    def test_step_into_wall_without_death_event_does_nothing(self):
        origin = PathFactory.make_chain("bf")
        sut = Snake(origin)
        sut._events = self._events
        try:
            sut.step()
        except Exception:
            self.fail("Snake death event threw an error")
