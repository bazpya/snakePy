from source.global_refs import CellType
from source.cell import Cell
from source.snake import Snake
from test.test_snake_ import Snake_


class Snake_step_(Snake_):
    # ===============================  step-blank  ===============================

    def test_step_when_into_blank_moves_head(self):
        destination = Cell()
        initial_head = Cell()
        initial_head.get_neighbour = lambda whatever: destination
        sut = Snake(initial_head, self._events)
        sut.step()
        self.assertEqual(destination, sut.get_head())

    def test_step_when_into_blank_makes_new_cell_snake(self):
        destination = Cell()
        initial_head = Cell()
        initial_head.get_neighbour = lambda whatever: destination
        sut = Snake(initial_head, self._events)
        sut.step()
        self.assertTrue(destination.is_snake)

    def test_step_when_into_blank_makes_tail_cell_blank(self):
        destination = Cell()
        initial_head = Cell()
        initial_head.get_neighbour = lambda whatever: destination
        sut = Snake(initial_head, self._events)
        initial_tail = sut.get_tail()
        sut.step()
        self.assertTrue(initial_tail.is_blank())

    def test_step_when_into_blank_keeps_length_same(self):
        destination = Cell()
        initial_head = Cell()
        initial_head.get_neighbour = lambda whatever: destination
        sut = Snake(initial_head, self._events)
        initial_length = sut.get_length()
        sut.step()
        self.assertEqual(initial_length, sut.get_length())

    # ===============================  step-food  ===============================

    def test_step_when_into_food_increments_length(self):
        destination = Cell(None, None, CellType.food)
        initial_head = Cell()
        initial_head.get_neighbour = lambda whatever: destination
        sut = Snake(initial_head, self._events)
        initial_length = sut.get_length()
        sut.step()
        self.assertEqual(initial_length + 1, sut.get_length())

    # ===============================  step-wall  ===============================

    def test_step_when_into_wall_without_death_event_does_nothing(self):
        destination = Cell(None, None, CellType.wall)
        initial_head = Cell()
        initial_head.get_neighbour = lambda whatever: destination
        sut = Snake(initial_head, self._events)
        try:
            sut.step()
        except Exception:
            self.fail("Snake death event threw an error")
