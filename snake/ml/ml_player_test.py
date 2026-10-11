from snake.core import Cell, Direction, Turn, WorldState
from snake.ml.ml_player import MLPlayer
from snake.ml.turn_estimates import TurnEstimates


def make_state(head: Cell = Cell(0, 0)) -> WorldState:
    return WorldState(
        end_cause=None,
        grid_cells=((Cell(0, 0), Cell(0, 1)),),
        snake_cells=frozenset({head}),
        head=head,
        tail=head,
        heading=Direction.right,
        last_turn=Turn.ahead,
        just_ate=False,
        food=None,
    )


class RecordingEye:
    # Sees a fixed sight; records the states it was shown
    def __init__(self, sight: list[float] = [0.5]) -> None:
        self._sight = sight
        self.states_seen: list[WorldState] = []

    def see(self, state: WorldState) -> list[float]:
        self.states_seen.append(state)
        return self._sight


class ScriptedBrain:
    # Gives fixed estimates; records the sights it was given
    def __init__(self, estimates: TurnEstimates = TurnEstimates(left=0.0, ahead=1.0, right=0.0)) -> None:
        self._estimates = estimates
        self.sights_seen: list[list[float]] = []

    def estimate(self, sight: list[float]) -> TurnEstimates:
        self.sights_seen.append(sight)
        return self._estimates


# ====================  Flow  ====================


def test_eye_gets_the_state():
    eye = RecordingEye()
    state = make_state()
    MLPlayer(eye, ScriptedBrain()).pick_turn(state)
    assert eye.states_seen == [state]


def test_brain_gets_what_the_eye_sees():
    brain = ScriptedBrain()
    MLPlayer(RecordingEye([0.1, 0.2]), brain).pick_turn(make_state())
    assert brain.sights_seen == [[0.1, 0.2]]


def test_each_call_uses_the_latest_state():
    eye = RecordingEye()
    sut = MLPlayer(eye, ScriptedBrain())
    first, second = make_state(Cell(0, 0)), make_state(Cell(0, 1))
    sut.pick_turn(first)
    sut.pick_turn(second)
    assert eye.states_seen == [first, second]


# ====================  Pick  ====================


def test_picks_the_best_turn_of_the_brains_estimates():
    estimates = TurnEstimates(left=0.1, ahead=0.2, right=0.9)
    sut = MLPlayer(RecordingEye(), ScriptedBrain(estimates))
    assert sut.pick_turn(make_state()) == Turn.right
