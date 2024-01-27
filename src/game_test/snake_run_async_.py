from src.game.snake import Snake
from src.game_test.helper.counter import Counter
from game_test.helper.cell_factory import CellFactory
from src.game_test.snake_ import Snake_


class Snake_run_async_(Snake_):
    async def test_run_async_when_specified_takes_correct_number_of_steps(self):
        counter = Counter()
        self._events.stepped.subscribe(counter.increment)

        origin = CellFactory.make_infinite_chain()
        sut = Snake(origin, self._small_number)
        sut._events = self._events
        await sut.run_async(self._msec)
        actual = counter.read()
        self.assertEqual(actual, self._small_number)

    async def test_run_async_into_snake_makes_snake_stop(self):
        counter = Counter()
        self._events.stepped.subscribe(counter.increment)
        pattern = "bbffbbs"
        origin = CellFactory.make_chain(pattern)
        sut = Snake(origin, self._large_number)
        sut._events = self._events
        await sut.run_async(self._msec)
        actual = counter.read()
        self.assertEqual(actual, len(pattern) - 1)
