from src.game.cell import Cell
from src.game.direction import Direction
from src.game.snake import Snake
from src.game_test.helper.path_factory import PathFactory
from src.game_test.snake_ import Snake_


class Snake_steering_(Snake_):
    def test_enque_and_deque_preserve_order(self):
        sut = Snake(Cell())
        sut._events = self._events
        for dir in Direction:
            sut.steering_enque(dir)

        for dir in Direction:
            self.assertEqual(sut._steering_deque(), dir)

    def test_enque_only_adds_if_perpendicular_to_previous(self):
        sut = Snake(Cell())
        sut._events = self._events
        for dir in Direction:
            sut.steering_enque(dir)
            sut.steering_enque(dir)
            sut.steering_enque(dir.get_opposite())

        self.assertEqual(len(sut._steering), len(Direction))

    def test_enque_with_empty_queue_only_adds_if_perpendicular_to_current(self):
        sut = Snake(Cell())
        sut._events = self._events
        for dir in Direction:
            sut._steering.clear()
            sut._direction = dir
            sut.steering_enque(dir)
            sut.steering_enque(dir.get_opposite())

        self.assertEqual(len(sut._steering), 0)

    def test_deque_when_empty_queue_gets_current_direction(self):
        origin = PathFactory.make_infinite_chain()
        sut = Snake(origin)
        sut._events = self._events
        for dir in Direction:
            sut._direction = dir
            sut.step()
            self.assertEqual(sut._direction, dir)
