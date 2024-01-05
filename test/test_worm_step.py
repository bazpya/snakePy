from source.global_refs import CellType
from source.cell import Cell
from source.worm import Worm
from test.test_worm_ import Worm_


class Worm_step_(Worm_):
    # ===============================  step-blank  ===============================

    def test_step_when_into_blank_moves_head(self):
        destination = Cell(None, None)
        initial_head = Cell(None, None)
        initial_head.get_neighbour = lambda whatever: destination
        sut = Worm(initial_head, self._events)
        sut.step()
        self.assertEqual(destination, sut.get_head())

    def test_step_when_into_blank_makes_new_cell_worm(self):
        destination = Cell(None, None)
        initial_head = Cell(None, None)
        initial_head.get_neighbour = lambda whatever: destination
        sut = Worm(initial_head, self._events)
        sut.step()
        self.assertTrue(destination.is_worm)

    def test_step_when_into_blank_makes_tail_cell_blank(self):
        destination = Cell(None, None)
        initial_head = Cell(None, None)
        initial_head.get_neighbour = lambda whatever: destination
        sut = Worm(initial_head, self._events)
        initial_tail = sut.get_tail()
        sut.step()
        self.assertTrue(initial_tail.is_blank())

    def test_step_when_into_blank_keeps_length_same(self):
        destination = Cell(None, None)
        initial_head = Cell(None, None)
        initial_head.get_neighbour = lambda whatever: destination
        sut = Worm(initial_head, self._events)
        initial_length = sut.get_length()
        sut.step()
        self.assertEqual(initial_length, sut.get_length())

    # ===============================  step-food  ===============================

    def test_step_when_into_food_increments_length(self):
        destination = Cell(None, None, CellType.food)
        initial_head = Cell(None, None)
        initial_head.get_neighbour = lambda whatever: destination
        sut = Worm(initial_head, self._events)
        initial_length = sut.get_length()
        sut.step()
        self.assertEqual(initial_length + 1, sut.get_length())

    # ===============================  step-wall  ===============================

    def test_step_when_into_wall_without_death_event_does_nothing(self):
        destination = Cell(None, None, CellType.wall)
        initial_head = Cell(None, None)
        initial_head.get_neighbour = lambda whatever: destination
        sut = Worm(initial_head, self._events)
        try:
            sut.step()
        except Exception:
            self.fail("Worm death event threw an error")
