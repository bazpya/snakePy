from source.global_refs import CellType
from source.cell import Cell
from source.worm import Worm
from test.test_worm_ import Worm_


class Worm_events_(Worm_):
    def test_step_when_into_blank_emits_the_right_events(self):
        destination = Cell(None, None, CellType.blank)
        initial_head = Cell(None, None)
        initial_head.get_neighbour = lambda whatever: destination
        sut = Worm(initial_head, self._events)
        sut.step()
        self.stepped_callback.assert_called()
        self.ate_callback.assert_not_called()
        self.died_callback.assert_not_called()

    def test_step_when_into_wall_emits_the_right_events(self):
        destination = Cell(None, None, CellType.wall)
        initial_head = Cell(None, None)
        initial_head.get_neighbour = lambda whatever: destination
        sut = Worm(initial_head, self._events)
        sut.step()
        self.stepped_callback.assert_called()
        self.ate_callback.assert_not_called()
        self.died_callback.assert_called()

    def test_step_when_into_worm_emits_the_right_events(self):
        destination = Cell(None, None, CellType.worm)
        initial_head = Cell(None, None)
        initial_head.get_neighbour = lambda whatever: destination
        sut = Worm(initial_head, self._events)
        sut.step()
        self.stepped_callback.assert_called()
        self.ate_callback.assert_not_called()
        self.died_callback.assert_called()

    def test_step_when_into_food_emits_the_right_events(self):
        destination = Cell(None, None, CellType.food)
        initial_head = Cell(None, None)
        initial_head.get_neighbour = lambda whatever: destination
        sut = Worm(initial_head, self._events)
        sut.step()
        self.stepped_callback.assert_called()
        self.ate_callback.assert_called()
        self.died_callback.assert_not_called()
