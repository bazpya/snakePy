from src.game.game import Game
from tests.game.game_ import Game_
from tests.game.helper.counter import Counter


class Game_etc_(Game_):
    def test_run_sync_at_specified_number_of_steps_emits_died_event(self):
        counter = Counter()
        sut = Game(self.row_count, self.col_count, steps_to_take=self.few)
        sut._events = self._events
        sut._events.stepped.subscribe(counter.increment)
        sut.run_sync()
        self.died_callback.assert_called_once()
        self.assertEqual(counter.read(), self.few)
