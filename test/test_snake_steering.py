from source.cell import Cell
from source.direction import Direction
from source.snake import Snake
from test.helper.path_factory import PathFactory
from test.test_snake_ import Snake_


class Snake_steering_(Snake_):
    def test_enque_and_deque_preserve_order(self):
        sut = Snake(Cell(), self._events)
        for dir in Direction:
            sut.steering_enque(dir)

        for dir in Direction:
            self.assertEqual(sut._steering_deque(), dir)

    def test_enque_only_adds_if_perpendicular_to_previous(self):
        sut = Snake(Cell(), self._events)
        for dir in Direction:
            sut.steering_enque(dir)
            sut.steering_enque(dir)
            sut.steering_enque(dir.get_opposite())

        self.assertEqual(len(sut._steering), len(Direction))

    def test_enque_with_empty_queue_only_adds_if_perpendicular_to_current(self):
        sut = Snake(Cell(), self._events)
        for dir in Direction:
            sut._steering.clear()
            sut._direction = dir
            sut.steering_enque(dir)
            sut.steering_enque(dir.get_opposite())

        self.assertEqual(len(sut._steering), 0)

    def test_deque_when_empty_queue_gets_current_direction(self):
        origin = PathFactory.make_infinite_chain()
        sut = Snake(origin, self._events)
        for dir in Direction:
            sut._direction = dir
            sut.step()
            self.assertEqual(sut._direction, dir)
