from source.snake import Snake
from test.helper.path_factory import PathFactory
from test.test_snake_ import Snake_


class Snake_step_(Snake_):
    # ===============================  step-blank  ===============================

    def test_step_when_into_blank_moves_head(self):
        cells = PathFactory.make_list("bb")
        PathFactory.link(cells)
        origin = cells[0]
        destination = cells[1]
        sut = Snake(origin, self._events)
        sut.step()
        self.assertEqual(destination, sut.get_head())

    def test_step_when_into_blank_makes_new_cell_snake(self):
        cells = PathFactory.make_list("bb")
        PathFactory.link(cells)
        origin = cells[0]
        destination = cells[1]
        sut = Snake(origin, self._events)
        sut.step()
        self.assertTrue(destination.is_snake())

    def test_step_when_into_blank_makes_tail_cell_blank(self):
        origin = PathFactory.make_chain("bb")
        sut = Snake(origin, self._events)
        sut.step()
        self.assertTrue(origin.is_blank())

    def test_step_when_into_blank_keeps_length_same(self):
        origin = PathFactory.make_chain("bb")
        sut = Snake(origin, self._events)
        initial_length = sut.get_length()
        sut.step()
        self.assertEqual(initial_length, sut.get_length())

    # ===============================  step-food  ===============================

    def test_step_when_into_food_increments_length(self):
        origin = PathFactory.make_chain("bf")
        sut = Snake(origin, self._events)
        initial_length = sut.get_length()
        sut.step()
        self.assertEqual(initial_length + 1, sut.get_length())

    # ===============================  step-wall  ===============================

    def test_step_when_into_wall_without_death_event_does_nothing(self):
        origin = PathFactory.make_chain("bf")
        sut = Snake(origin, self._events)
        try:
            sut.step()
        except Exception:
            self.fail("Snake death event threw an error")
