from unittest.mock import MagicMock
from src.ml.player import Player
from tests.ml.player_ import Player_


class Player_Etc_(Player_):

    def test_save_proxies_brain_save(self):
        sut = Player(1)
        stub = MagicMock()
        sut._brain.save = stub
        sut.save()
        stub.assert_called_once()
