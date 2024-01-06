from source.global_refs import CellType
from source.cell import Cell
from source.snake import Snake
from test.test_snake_ import Snake_


class Snake_events_(Snake_):
    def test_step_when_into_blank_emits_the_right_events(self):
        destination = Cell(None, None, CellType.blank)
        initial_head = Cell(None, None)
        initial_head.get_neighbour = lambda whatever: destination
        sut = Snake(initial_head, self._events)
        sut.step()
        self.stepped_callback.assert_called()
        self.ate_callback.assert_not_called()
        self.died_callback.assert_not_called()

    def test_step_when_into_blank_passes_changed_cells_to_event(self):
        destination = Cell(None, None)
        initial_head = Cell(None, None)
        initial_head.get_neighbour = lambda whatever: destination
        sut = Snake(initial_head, self._events)
        sut.step()
        self.stepped_callback.assert_called_with([destination, initial_head])

    def test_step_when_into_wall_emits_the_right_events(self):
        destination = Cell(None, None, CellType.wall)
        initial_head = Cell(None, None)
        initial_head.get_neighbour = lambda whatever: destination
        sut = Snake(initial_head, self._events)
        sut.step()
        self.stepped_callback.assert_called()
        self.ate_callback.assert_not_called()
        self.died_callback.assert_called()

    def test_step_when_into_snake_emits_the_right_events(self):
        destination = Cell(None, None, CellType.snake)
        initial_head = Cell(None, None)
        initial_head.get_neighbour = lambda whatever: destination
        sut = Snake(initial_head, self._events)
        sut.step()
        self.stepped_callback.assert_called()
        self.ate_callback.assert_not_called()
        self.died_callback.assert_called()

    def test_step_when_into_food_emits_the_right_events(self):
        destination = Cell(None, None, CellType.food)
        initial_head = Cell(None, None)
        initial_head.get_neighbour = lambda whatever: destination
        sut = Snake(initial_head, self._events)
        sut.step()
        self.stepped_callback.assert_called()
        self.ate_callback.assert_called()
        self.died_callback.assert_not_called()

    def test_step_when_into_food_passes_changed_cells_to_event(self):
        destination = Cell(None, None, CellType.food)
        initial_head = Cell(None, None)
        initial_head.get_neighbour = lambda whatever: destination
        sut = Snake(initial_head, self._events)
        sut.step()
        self.stepped_callback.assert_called_with([destination])
