from source.snake import Snake
from test.helper.counter import Counter
from test.helper.path_factory import PathFactory
from test.test_snake_ import Snake_


class Snake_run_(Snake_):
    async def test_run_when_specified_takes_correct_number_of_steps(self):
        counter = Counter()
        self._events.stepped.subscribe(counter.increment)

        origin = PathFactory.make_infinite_chain()
        sut = Snake(origin, self._events)
        await sut.run(self._msec, self._some_number_1)
        actual = counter.read()
        self.assertEqual(actual, self._some_number_1)
