from snake.core import Cell, Direction, StepResult, Turn
from snake.ml.ml_player import MLPlayer
from snake.ml.turn_scores import TurnScores


def make_result(head: Cell = Cell(0, 0)) -> StepResult:
    return StepResult(
        is_over=False,
        cell_rows=((Cell(0, 0), Cell(0, 1)),),
        snake_cells=frozenset({head}),
        head=head,
        direction=Direction.right,
        food=None,
    )


class RecordingEye:
    # Sees a fixed state; records the results it was shown
    def __init__(self, state: list[float] = [0.5]) -> None:
        self._state = state
        self.results_seen: list[StepResult] = []

    def see(self, result: StepResult) -> list[float]:
        self.results_seen.append(result)
        return self._state


class ScriptedBrain:
    # Gives fixed scores; records the states it was given
    def __init__(self, scores: TurnScores = TurnScores(left=0.0, ahead=1.0, right=0.0)) -> None:
        self._scores = scores
        self.states_seen: list[list[float]] = []

    def score(self, state: list[float]) -> TurnScores:
        self.states_seen.append(state)
        return self._scores


# ====================  Flow  ====================


def test_eye_gets_the_result():
    eye = RecordingEye()
    result = make_result()
    MLPlayer(eye, ScriptedBrain()).pick_turn(result)
    assert eye.results_seen == [result]


def test_brain_gets_what_the_eye_sees():
    brain = ScriptedBrain()
    MLPlayer(RecordingEye([0.1, 0.2]), brain).pick_turn(make_result())
    assert brain.states_seen == [[0.1, 0.2]]


def test_each_call_uses_the_latest_result():
    eye = RecordingEye()
    sut = MLPlayer(eye, ScriptedBrain())
    first, second = make_result(Cell(0, 0)), make_result(Cell(0, 1))
    sut.pick_turn(first)
    sut.pick_turn(second)
    assert eye.results_seen == [first, second]


# ====================  Pick  ====================


def test_picks_the_best_turn_of_the_brains_scores():
    scores = TurnScores(left=0.1, ahead=0.2, right=0.9)
    sut = MLPlayer(RecordingEye(), ScriptedBrain(scores))
    assert sut.pick_turn(make_result()) == Turn.right
