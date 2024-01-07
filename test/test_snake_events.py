from source.global_refs import CellType
from source.cell import Cell
from source.snake import Snake
from test.test_snake_ import Snake_


class Snake_events_(Snake_):
    # ======================  Events  ======================

    def test_step_into_blank_emits_the_right_events(self):
        destination = Cell(None, None, CellType.blank)
        initial_head = Cell()
        initial_head.get_neighbour = lambda whatever: destination
        sut = Snake(initial_head, self._events)
        sut.step()
        self.stepped_callback.assert_called()
        self.ate_callback.assert_not_called()
        self.died_callback.assert_not_called()

    def test_step_into_wall_emits_the_right_events(self):
        destination = Cell(None, None, CellType.wall)
        initial_head = Cell()
        initial_head.get_neighbour = lambda whatever: destination
        sut = Snake(initial_head, self._events)
        sut.step()
        self.stepped_callback.assert_called()
        self.ate_callback.assert_not_called()
        self.died_callback.assert_called()

    def test_step_into_snake_emits_the_right_events(self):
        destination = Cell(None, None, CellType.snake)
        initial_head = Cell()
        initial_head.get_neighbour = lambda whatever: destination
        sut = Snake(initial_head, self._events)
        sut.step()
        self.stepped_callback.assert_called()
        self.ate_callback.assert_not_called()
        self.died_callback.assert_called()

    def test_step_when_into_food_emits_the_right_events(self):
        destination = Cell(None, None, CellType.food)
        initial_head = Cell()
        initial_head.get_neighbour = lambda whatever: destination
        sut = Snake(initial_head, self._events)
        sut.step()
        self.stepped_callback.assert_called()
        self.ate_callback.assert_called()
        self.died_callback.assert_not_called()

    # ======================  Changed Cells  ======================

    def test_step_into_blank_passes_changed_cells_to_stepped_event(self):
        destination = Cell()
        initial_head = Cell()
        initial_head.get_neighbour = lambda whatever: destination
        sut = Snake(initial_head, self._events)
        sut.step()
        self.stepped_callback.assert_called_with([destination, initial_head])

    def test_step_into_food_passes_changed_cells_to_stepped_event(self):
        destination = Cell(None, None, CellType.food)
        initial_head = Cell()
        initial_head.get_neighbour = lambda whatever: destination
        sut = Snake(initial_head, self._events)
        sut.step()
        self.stepped_callback.assert_called_with([destination])

    def test_step_into_wall_passes_no_cells_to_stepped_event(self):
        destination = Cell(None, None, CellType.wall)
        initial_head = Cell()
        initial_head.get_neighbour = lambda whatever: destination
        sut = Snake(initial_head, self._events)
        sut.step()
        self.stepped_callback.assert_called_with([])

    def test_step_into_snake_passes_no_cells_to_stepped_event(self):
        destination = Cell(None, None, CellType.snake)
        initial_head = Cell()
        initial_head.get_neighbour = lambda whatever: destination
        sut = Snake(initial_head, self._events)
        sut.step()
        self.stepped_callback.assert_called_with([])

    # ======================  Death  ======================

    def test_passes_length_to_died_event(self):
        destination = Cell(None, None, CellType.wall)
        initial_head = Cell()
        initial_head.get_neighbour = lambda whatever: destination
        sut = Snake(initial_head, self._events)
        sut.step()
        self.died_callback.assert_called_with(1)
