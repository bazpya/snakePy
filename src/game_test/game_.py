import unittest
from unittest.mock import MagicMock
from src.game.game import Game
from src.game.event import Event
from src.game.event_hub import EventHub


class Game_(unittest.TestCase):
    _some_number_1 = 7
    _some_number_2 = 10
    _sut: Game

    def __init__(self, *args, **kwargs):
        super(Game_, self).__init__(*args, **kwargs)
        self.row_count = 2 * self._some_number_1
        self.col_count = 2 * self._some_number_2

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

        self._events.ready_to_draw = Event()
        self.ready_to_draw_callback = MagicMock()
        self._events.ready_to_draw.subscribe(self.ready_to_draw_callback)

    def setUp(self):
        self._sut = Game(self.row_count, self.col_count)
