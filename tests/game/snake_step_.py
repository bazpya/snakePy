from unittest.mock import MagicMock
from src.game.cell import Cell
from src.game.direction import Direction
from src.game.snake import Snake
from src.game.result import SnakeResult
from tests.game.helper.cell_factory import CellFactory
from tests.game.snake_ import Snake_sync_


class Snake_step_(Snake_sync_):
    # ===============================  step-blank  ===============================

    def test_step_into_blank_moves_head(self):
        origin, cells = CellFactory.make("bb")
        destination = cells[1]
        sut = Snake(origin)
        sut._events = self._events
        sut.step()
        self.assertEqual(destination, sut.get_head())

    def test_step_into_blank_makes_new_cell_snake(self):
        origin, cells = CellFactory.make("bbbf")
        destination = cells[1]
        sut = Snake(origin)
        sut._events = self._events
        sut.step()
        self.assertTrue(destination.is_snake())

    def test_step_into_blank_makes_tail_cell_blank(self):
        origin, *etc = CellFactory.make("bbbf")
        sut = Snake(origin)
        sut._events = self._events
        sut.step()
        self.assertTrue(origin.is_blank())

    def test_step_into_blank_keeps_length_same(self):
        origin, *etc = CellFactory.make("bbbf")
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
        origin = CellFactory.make_infinite_chain()
        sut = Snake(origin, self.some)
        sut._events = self._events
        sut.run_sync()
        result: SnakeResult = self.died_callback.call_args[0][0]
        self.assertEqual(result.steps_taken, self.some)

    # ===============================  step-food  ===============================

    def test_step_into_food_leaves_tail_cell_snake(self):
        origin, *etc = CellFactory.make("bffff")
        sut = Snake(origin)
        sut._events = self._events
        sut.step()
        self.assertTrue(origin.is_snake())

    def test_step_into_food_increments_length(self):
        origin, *etc = CellFactory.make("bffff")
        sut = Snake(origin)
        sut._events = self._events
        initial_length = sut.get_length()
        sut.step()
        self.assertEqual(initial_length + 1, sut.get_length())

    def test_step_into_food_when_reached_step_count_dies(self):
        origin, *etc = CellFactory.make("f" * (self.many))
        sut = Snake(origin, self.some)
        sut._events = self._events
        sut.run_sync()
        result: SnakeResult = self.died_callback.call_args[0][0]
        self.assertEqual(result.steps_taken, self.some)

    # ===============================  step-death  ===============================

    def test_step_into_wall_without_death_event_does_nothing(self):
        origin, *etc = CellFactory.make("bf")
        sut = Snake(origin)
        sut._events = self._events
        try:
            sut.step()
        except Exception:
            self.fail("Snake death event threw an error")

    # ===============================  step-any  ===============================

    def test_step_adds_to_visited_cells(self):
        origin, cells = CellFactory.make("bbbw")
        sut = Snake(origin)
        sut.run_sync()
        self.assertSetEqual(sut._cells_visited, set(cells[:-1]))
