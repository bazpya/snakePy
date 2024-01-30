from tests.test_ import Test_
from unittest.mock import MagicMock
from src.game.cell import Cell
from src.game.global_refs import CellType
from src.game.game import Game
from src.game.event import Event
from src.game.event_hub import EventHub


class Game_(Test_):
    sut: Game

    def __init__(self, *args, **kwargs):
        super(Game_, self).__init__(*args, **kwargs)
        self.row_count = 2 * self.some
        self.col_count = 2 * self.many

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

    def setUp(self):
        self.sut = Game(self.row_count, self.col_count)
        self.sut.events = self._events

    def assertCellCount(self, game: Game, cell_type: CellType, expected: int):
        def counter_func(cell: Cell, ri, ci, acc):
            return acc + 1 if cell._type == cell_type else acc

        actual = game.iterate_cells(False, counter_func, 0)
        self.assertEqual(actual, expected)
