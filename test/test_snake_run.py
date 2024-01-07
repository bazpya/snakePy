from source.cell import Cell
from source.snake import Snake
from test.helper.counter import Counter
from test.test_snake_ import Snake_


class Snake_run_(Snake_):
    def neighbour_getter(self, *args):
        neighbour = Cell(None, None)
        neighbour.get_neighbour = self.neighbour_getter
        return neighbour

    async def test_run_when_specified_takes_correct_number_of_steps(self):
        counter = Counter()
        self._events.stepped.subscribe(counter.increment)

        initial_head = Cell(None, None)
        initial_head.get_neighbour = self.neighbour_getter
        sut = Snake(initial_head, self._events)
        await sut.run(self._msec, self._some_number_1)
        actual = counter.read()
        self.assertEqual(actual, self._some_number_1)
