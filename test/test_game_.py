import unittest
from source.global_refs import Direction, CellType
from source.game import Game
from source.cell import Cell

row_count = 17
col_count = 18
initial_sut = Game(row_count, col_count)


class Game_(unittest.TestCase):
    def get_new_sut(*args, **kwargs):
        return Game(row_count, col_count)
