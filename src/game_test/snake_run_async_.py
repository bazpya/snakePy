from src.game.snake import Snake
from src.game_test.helper.counter import Counter
from src.game_test.helper.path_factory import PathFactory
from src.game_test.snake_ import Snake_


class Snake_run_async_(Snake_):
    async def test_run_async_when_specified_takes_correct_number_of_steps(self):
        counter = Counter()
        self._events.stepped.subscribe(counter.increment)

        origin = PathFactory.make_infinite_chain()
        sut = Snake(origin)
        sut._events = self._events
        await sut.run_async(self._msec, self._some_number_1)
        actual = counter.read()
        self.assertEqual(actual, self._some_number_1)

    async def test_run_async_into_snake_makes_snake_stop(self):
        counter = Counter()
        self._events.stepped.subscribe(counter.increment)
        path_pattern = "bbffbbs"
        origin = PathFactory.make_chain(path_pattern)
        sut = Snake(origin)
        sut._events = self._events
        await sut.run_async(self._msec, 20)
        actual = counter.read()
        self.assertEqual(actual, len(path_pattern) - 1)
