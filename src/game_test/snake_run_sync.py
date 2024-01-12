from src.game.snake import Snake
from src.game_test.helper.counter import Counter
from src.game_test.helper.path_factory import PathFactory
from src.game_test.snake_ import Snake_


class Snake_run_sync_(Snake_):
    def test_run_sync_when_specified_takes_correct_number_of_steps(self):
        counter = Counter()
        self._events.stepped.subscribe(counter.increment)

        origin = PathFactory.make_infinite_chain()
        sut = Snake(origin, self._events)
        sut.run_sync(self._some_number_1)
        actual = counter.read()
        self.assertEqual(actual, self._some_number_1)

    def test_run_sync_into_snake_makes_snake_stop(self):
        counter = Counter()
        self._events.stepped.subscribe(counter.increment)
        path_pattern = "bbffbbs"
        origin = PathFactory.make_chain(path_pattern)
        sut = Snake(origin, self._events)
        sut.run_sync(20)
        actual = counter.read()
        self.assertEqual(actual, len(path_pattern) - 1)
