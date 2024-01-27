from src.game.snake import Snake
from tests.game.helper.counter import Counter
from tests.game.helper.cell_factory import CellFactory
from tests.game.snake_ import Snake_sync_


class Snake_run_sync_(Snake_sync_):
    def test_run_sync_when_specified_takes_correct_number_of_steps(self):
        counter = Counter()
        origin = CellFactory.make_infinite_chain()
        sut = Snake(origin, self.few)
        sut._events.stepped.subscribe(counter.increment)
        sut.run_sync()
        actual = counter.read()
        self.assertEqual(actual, self.few)

    def test_run_sync_into_death_makes_snake_stop(self):
        counter = Counter()
        pattern = "bbffbbs"
        origin = CellFactory.make_chain(pattern)
        sut = Snake(origin)
        sut._events.stepped.subscribe(counter.increment)
        sut.run_sync()
        actual = counter.read()
        self.assertEqual(actual, len(pattern) - 1)
