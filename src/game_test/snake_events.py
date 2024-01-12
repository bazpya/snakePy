from src.game.snake import Snake
from src.game_test.helper.path_factory import PathFactory
from src.game_test.snake_ import Snake_


class Snake_events_(Snake_):
    # ======================  Events  ======================

    def test_step_into_blank_emits_the_right_events(self):
        first_cell = PathFactory.make_chain("bb")
        sut = Snake(first_cell, self._events)
        sut.step()
        self.stepped_callback.assert_called()
        self.ate_callback.assert_not_called()
        self.died_callback.assert_not_called()

    def test_step_into_wall_emits_the_right_events(self):
        first_cell = PathFactory.make_chain("bw")
        sut = Snake(first_cell, self._events)
        sut.step()
        self.stepped_callback.assert_called()
        self.ate_callback.assert_not_called()
        self.died_callback.assert_called()

    def test_step_into_snake_emits_the_right_events(self):
        first_cell = PathFactory.make_chain("bs")
        sut = Snake(first_cell, self._events)
        sut.step()
        self.stepped_callback.assert_called()
        self.ate_callback.assert_not_called()
        self.died_callback.assert_called()

    def test_step_when_into_food_emits_the_right_events(self):
        first_cell = PathFactory.make_chain("bf")
        sut = Snake(first_cell, self._events)
        sut.step()
        self.stepped_callback.assert_called()
        self.ate_callback.assert_called()
        self.died_callback.assert_not_called()

    # ======================  Changed Cells  ======================

    def test_step_into_blank_passes_changed_cells_to_stepped_event(self):
        cells = PathFactory.make_list("bb")
        PathFactory.link(cells)
        origin = cells[0]
        destination = cells[1]
        sut = Snake(origin, self._events)
        sut.step()
        self.stepped_callback.assert_called_with([destination, origin])

    def test_step_into_food_passes_changed_cells_to_stepped_event(self):
        cells = PathFactory.make_list("bf")
        PathFactory.link(cells)
        origin = cells[0]
        destination = cells[1]
        sut = Snake(origin, self._events)
        sut.step()
        self.stepped_callback.assert_called_with([destination])

    def test_step_into_wall_passes_no_cells_to_stepped_event(self):
        cells = PathFactory.make_list("bw")
        PathFactory.link(cells)
        origin = cells[0]
        sut = Snake(origin, self._events)
        sut.step()
        self.stepped_callback.assert_called_with([])

    def test_step_into_snake_passes_no_cells_to_stepped_event(self):
        cells = PathFactory.make_list("bs")
        PathFactory.link(cells)
        origin = cells[0]
        sut = Snake(origin, self._events)
        sut.step()
        self.stepped_callback.assert_called_with([])

    # ======================  Death  ======================

    def test_passes_length_to_died_event_single(self):
        first_cell = PathFactory.make_chain("bw")
        sut = Snake(first_cell, self._events)
        sut.step()
        self.died_callback.assert_called_with(1)

    def test_passes_length_to_died_event(self):
        path_pattern = "bbffbbs"
        path_handle = PathFactory.make_chain(path_pattern)
        sut = Snake(path_handle, self._events)
        for i in range(0, 6):
            sut.step()
        self.died_callback.assert_called_with(3)

    # ======================  ?????  ======================
