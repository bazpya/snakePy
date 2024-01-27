from src.game.global_refs import CauseOfDeath
from src.game.snake import Snake
from src.game.Result import SnakeResult
from tests.game.helper.cell_factory import CellFactory
from tests.game.snake_ import Snake_sync_


class Snake_result_(Snake_sync_):
    # ======================  Steps Taken  ======================

    def test_emits_died_event_with_correct_number_of_steps_single(self):
        origin = CellFactory.make_chain("bw")
        sut = Snake(origin)
        sut._events = self._events
        sut.run_sync()
        result: SnakeResult = self.died_callback.call_args[0][0]
        self.assertEqual(result.steps_taken, 1)

    def test_emits_died_event_with_correct_number_of_steps_multi(self):
        pattern = "bbffbbs"
        origin = CellFactory.make_chain(pattern)
        sut = Snake(origin)
        sut._events = self._events
        sut.run_sync()
        result: SnakeResult = self.died_callback.call_args[0][0]
        self.assertEqual(result.steps_taken, len(pattern) - 1)

    # ======================  Length  ======================

    def test_emits_died_event_with_correct_length_single(self):
        origin = CellFactory.make_chain("bw")
        sut = Snake(origin)
        sut._events = self._events
        sut.run_sync()
        result: SnakeResult = self.died_callback.call_args[0][0]
        self.assertEqual(result.length, 1)

    def test_emits_died_event_with_correct_length_multi(self):
        pattern = "bbffbbs"
        origin = CellFactory.make_chain(pattern)
        sut = Snake(origin)
        sut._events = self._events
        sut.run_sync()
        result: SnakeResult = self.died_callback.call_args[0][0]
        self.assertEqual(result.length, 3)

    # ======================  Cause of Death  ======================

    def test_emits_died_event_with_cause_of_death_wall(self):
        origin = CellFactory.make_chain("bbbfbbw")
        sut = Snake(origin)
        sut._events = self._events
        sut.run_sync()
        result: SnakeResult = self.died_callback.call_args[0][0]
        self.assertEqual(result.cause_of_death, CauseOfDeath.wall)

    def test_emits_died_event_with_cause_of_death_snake(self):
        origin = CellFactory.make_chain("bbbfbbs")
        sut = Snake(origin)
        sut._events = self._events
        sut.run_sync()
        result: SnakeResult = self.died_callback.call_args[0][0]
        self.assertEqual(result.cause_of_death, CauseOfDeath.snake)
