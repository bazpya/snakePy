import unittest
from unittest.mock import MagicMock
from source.event import Event
from source.event_hub import EventHub
from source.global_refs import CellType
from source.cell import Cell
from source.worm import Worm


class Worm_(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(Worm_, self).__init__(*args, **kwargs)

        self._events = EventHub()

        self._events.stepped = Event()
        self.stepped_callback = MagicMock()
        self._events.stepped.subscribe(self.stepped_callback)

        self._events.ate = Event()
        self.ate_callback = MagicMock()
        self._events.ate.subscribe(self.ate_callback)

        self._events.died = Event()
        self.died_callback = MagicMock()
        self._events.died.subscribe(self.died_callback)

    # ===============================  init  ===============================

    def test_init_sets_one_cell_only(self):
        cell = Cell(None, None)
        sut = Worm(cell)
        self.assertEqual(1, sut.get_length())

    # ===============================  events  ===============================

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

    # ===============================  step-blank  ===============================

    def test_step_moves_head(self):
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
