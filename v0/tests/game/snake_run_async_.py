from src.game.snake import Snake
from tests.game.helper.counter import Counter
from tests.game.helper.cell_factory import CellFactory
from tests.game.snake_ import Snake_async_


class Snake_run_async_(Snake_async_):
    async def test_run_async_when_specified_takes_correct_number_of_steps(self):
        counter = Counter()
        self._events.stepped.subscribe(counter.increment)
        origin = CellFactory.make_infinite_chain()
        sut = Snake(origin, self.few)
        sut._events = self._events
        await sut.run_async()
        actual = counter.read()
        self.assertEqual(actual, self.few)

    async def test_run_async_into_death_makes_snake_stop(self):
        counter = Counter()
        self._events.stepped.subscribe(counter.increment)
        pattern = "bbffbbs"
        origin, *etc = CellFactory.make(pattern)
        sut = Snake(origin)
        sut._events = self._events
        await sut.run_async()
        actual = counter.read()
        self.assertEqual(actual, len(pattern) - 1)

    async def test_run_async_into_death_emits_died_event(self):
        origin, *etc = CellFactory.make("bbffbbs")
        sut = Snake(origin)
        sut._events = self._events
        await sut.run_async()
        self.died_callback.assert_called_once()
