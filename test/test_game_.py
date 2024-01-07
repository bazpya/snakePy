import unittest
from source.game import Game


class Game_(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(Game_, self).__init__(*args, **kwargs)
        self.row_count = 17
        self.col_count = 18

    def make_sut(self, *args, **kwargs):
        return Game(self.row_count, self.col_count)
