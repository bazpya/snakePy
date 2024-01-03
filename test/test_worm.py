import unittest
from unittest.mock import MagicMock
from source.event import Event
from source.global_refs import CellType
from source.cell import Cell
from source.worm import Worm


class Worm_(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(Worm_, self).__init__(*args, **kwargs)
        self.step_event = Event()
        self.step_callback = MagicMock()
        self.step_event.subscribe(self.step_callback)

        self.ate_event = Event()
        self.ate_callback = MagicMock()
        self.ate_event.subscribe(self.ate_callback)

        self.death_event = Event()
        self.death_callback = MagicMock()
        self.death_event.subscribe(self.death_callback)

    # ===============================  init  ===============================

    def test_init_sets_one_cell_only(self):
        cell = Cell(None, None)
        sut = Worm(cell)
        self.assertEqual(1, sut.get_length())

    # ===============================  step-any  ===============================

    def test_step_when_into_any_cell_emits_step_event(self):
        for cellType in CellType:
            destination = Cell(None, None, cellType)
            initial_head = Cell(None, None)
            initial_head.get_neighbour = lambda whatever: destination
            sut = Worm(initial_head, self.step_event, self.ate_event, self.death_event)
            sut.step()
            self.step_callback.assert_called()

    # ===============================  step-blank  ===============================

    def test_step_moves_head(self):
        destination = Cell(None, None)
        initial_head = Cell(None, None)
        initial_head.get_neighbour = lambda whatever: destination
        sut = Worm(initial_head, self.step_event, self.ate_event, self.death_event)
        sut.step()
        self.assertEqual(destination, sut.get_head())

    def test_step_when_into_blank_makes_new_cell_worm(self):
        destination = Cell(None, None)
        initial_head = Cell(None, None)
        initial_head.get_neighbour = lambda whatever: destination
        sut = Worm(initial_head, self.step_event, self.ate_event, self.death_event)
        sut.step()
        self.assertTrue(destination.is_worm)

    def test_step_when_into_blank_makes_tail_cell_blank(self):
        destination = Cell(None, None)
        initial_head = Cell(None, None)
        initial_head.get_neighbour = lambda whatever: destination
        sut = Worm(initial_head, self.step_event, self.ate_event, self.death_event)
        initial_tail = sut.get_tail()
        sut.step()
        self.assertTrue(initial_tail.is_blank())

    def test_step_when_into_blank_keeps_length_same(self):
        destination = Cell(None, None)
        initial_head = Cell(None, None)
        initial_head.get_neighbour = lambda whatever: destination
        sut = Worm(initial_head, self.step_event, self.ate_event, self.death_event)
        initial_length = sut.get_length()
        sut.step()
        self.assertEqual(initial_length, sut.get_length())

    # ===============================  step-food  ===============================

    def test_step_when_into_food_increments_length(self):
        destination = Cell(None, None, CellType.food)
        initial_head = Cell(None, None)
        initial_head.get_neighbour = lambda whatever: destination
        sut = Worm(initial_head, self.step_event, self.ate_event, self.death_event)
        initial_length = sut.get_length()
        sut.step()
        self.assertEqual(initial_length + 1, sut.get_length())

    def test_step_when_into_food_emits_ate_event(self):
        destination = Cell(None, None, CellType.food)
        initial_head = Cell(None, None)
        initial_head.get_neighbour = lambda whatever: destination
        sut = Worm(initial_head, self.step_event, self.ate_event, self.death_event)
        sut.step()
        self.step_callback.assert_called()
        self.ate_callback.assert_called()

    def test_step_when_into_food_does_not_emit_death_event(self):
        destination = Cell(None, None, CellType.food)
        initial_head = Cell(None, None)
        initial_head.get_neighbour = lambda whatever: destination
        sut = Worm(initial_head, self.step_event, self.ate_event, self.death_event)
        sut.step()
        self.death_callback.assert_not_called()

    # ===============================  step-wall  ===============================

    def test_step_when_into_wall_emit_death_event(self):
        destination = Cell(None, None, CellType.wall)
        initial_head = Cell(None, None)
        initial_head.get_neighbour = lambda whatever: destination
        sut = Worm(initial_head, self.step_event, self.ate_event, self.death_event)
        sut.step()
        self.death_callback.assert_called()

    def test_step_when_into_wall_without_death_event_does_nothing(self):
        destination = Cell(None, None, CellType.wall)
        initial_head = Cell(None, None)
        initial_head.get_neighbour = lambda whatever: destination
        sut = Worm(initial_head, self.step_event, self.ate_event, self.death_event)
        try:
            sut.step()
        except Exception:
            self.fail("Worm death event threw an error")
