from src.game.global_refs import CauseOfDeath
from src.game.direction import Turn
from src.game.Result import GameResult
from src.game.snake import Snake
from tests.game.game_ import Game_
from tests.game.helper.cell_factory import CellFactory


class Game_result_(Game_):
    def test_emits_died_event_with_correct_number_of_steps(self):
        pattern = "bbffbbs"
        origin = CellFactory.make_chain(pattern)
        snake = Snake(origin)
        self._sut._bind(snake)
        snake.run_sync()
        result: GameResult = self.died_callback.call_args[0][0]
        self.assertEqual(result.steps_taken, len(pattern) - 1)

    def test_emits_died_event_with_correct_length(self):
        pattern = "bbffbbs"
        origin = CellFactory.make_chain(pattern)
        snake = Snake(origin)
        self._sut._bind(snake)
        snake.run_sync()
        result: GameResult = self.died_callback.call_args[0][0]
        self.assertEqual(result.length, 3)

    def test_emits_died_event_with_correct_cause_of_death(self):
        pattern = "bbffbbs"
        origin = CellFactory.make_chain(pattern)
        snake = Snake(origin)
        self._sut._bind(snake)
        snake.run_sync()
        result: GameResult = self.died_callback.call_args[0][0]
        self.assertEqual(result.cause_of_death, CauseOfDeath.snake)

    # todo: use recorder object instead
    def test_death_passes_turs_taken_to_died_event(self):
        turns = [Turn.left, Turn.right, Turn.ahead, Turn.ahead, Turn.right]
        for turn in turns:
            self._sut.turn(turn)
        self._sut.run_sync()
        self.died_callback.assert_called_once()
        result: GameResult = self.died_callback.call_args[0][0]
        self.assertEqual(result.turns, turns)

    # todo: use recorder object instead
    def test_death_passes_correct_number_of_foods_taken_to_died_event(self):
        pattern = "bbffbbs"
        origin = CellFactory.make_chain(pattern)
        snake = Snake(origin)
        self._sut._bind(snake)
        snake.run_sync()
        result: GameResult = self.died_callback.call_args[0][0]
        self.assertEqual(len(result.foods), 3)
