from src.game.cell import Cell
from src.game.direction import Direction, Turn
from src.game.snake import Snake
from src.game_test.helper.path_factory import PathFactory
from src.game_test.snake_ import Snake_


class Snake_directions_(Snake_):
    def test_enque_and_deque_preserve_order(self):
        sut = Snake(Cell())
        for dir in Direction:
            sut.direction_enque(dir)

        for dir in Direction:
            self.assertEqual(sut._direction_deque(), dir)

    def test_enque_only_adds_if_perpendicular_to_previous(self):
        sut = Snake(Cell())
        for dir in Direction:
            sut.direction_enque(dir)
            sut.direction_enque(dir)
            sut.direction_enque(dir.get_opposite())

        self.assertEqual(len(sut._directions), len(Direction))

    def test_enque_with_empty_queue_only_adds_if_perpendicular_to_current(self):
        sut = Snake(Cell())
        sut._directions.clear()
        for dir in Direction:
            sut._direction = dir
            sut.direction_enque(dir)
            sut.direction_enque(dir.get_opposite())
            self.assertEqual(len(sut._directions), 0)

    def test_deque_when_empty_queue_gets_current_direction(self):
        origin = PathFactory.make_infinite_chain()
        sut = Snake(origin)
        for dir in Direction:
            sut._direction = dir
            sut.step()
            self.assertEqual(sut._direction, dir)

    def test_turn_enqueues_direction(self):
        sut = Snake(Cell())
        for dir in Direction:
            sut._directions.clear()
            sut._direction = dir
            for turn in Turn:
                sut.turn(turn)
            self.assertEqual(len(sut._directions), len(Turn) - 1)
