from tests.test_ import Test_
from unittest.mock import MagicMock
from src.game.cell import Cell
from src.game.global_refs import CellType
from src.game.game import Game


class Game_(Test_):
    def __init__(self, *args, **kwargs):
        super(Game_, self).__init__(*args, **kwargs)
        self.stepped_callback = MagicMock()
        self.ate_callback = MagicMock()
        self.died_callback = MagicMock()

    def setUp(self):
        self.sut = Game()
        self.sut.events.stepped.subscribe(self.stepped_callback)
        self.sut.events.ate.subscribe(self.ate_callback)
        self.sut.events.died.subscribe(self.died_callback)

    def assertCellCount(self, game: Game, cell_type: CellType, expected: int):
        def counter_func(cell: Cell, ri, ci, acc):
            return acc + 1 if cell.type == cell_type else acc

        actual = game.iterate_cells(False, counter_func, 0)
        self.assertEqual(actual, expected)
