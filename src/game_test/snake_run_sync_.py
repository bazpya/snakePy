from src.game.snake import Snake
from src.game_test.helper.counter import Counter
from game_test.helper.cell_factory import CellFactory
from src.game_test.snake_ import Snake_


class Snake_run_sync_(Snake_):
    def test_run_sync_when_specified_takes_correct_number_of_steps(self):
        counter = Counter()
        origin = CellFactory.make_infinite_chain()
        sut = Snake(origin, self._small_number)
        sut._events.stepped.subscribe(counter.increment)
        sut.run_sync()
        actual = counter.read()
        self.assertEqual(actual, self._small_number)

    def test_run_sync_into_death_makes_snake_stop(self):
        counter = Counter()
        pattern = "bbffbbs"
        origin = CellFactory.make_chain(pattern)
        sut = Snake(origin)
        sut._events.stepped.subscribe(counter.increment)
        sut.run_sync()
        actual = counter.read()
        self.assertEqual(actual, len(pattern) - 1)
