from unittest.mock import MagicMock
from src.game.event import Event
from src.game.event_hub import EventHub
from tests.test_ import Test_, Test_async_


class Snake_sync_(Test_):
    def __init__(self, *args, **kwargs):
        super(Snake_sync_, self).__init__(*args, **kwargs)

    def setUp(self):
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


class Snake_async_(Test_async_):
    def __init__(self, *args, **kwargs):
        super(Snake_async_, self).__init__(*args, **kwargs)

    def setUp(self):
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
