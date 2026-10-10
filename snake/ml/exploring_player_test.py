import random
import pytest
from snake.core import Cell, Direction, StepResult, Turn
from snake.ml.exploring_player import ExploringPlayer

RESULT = StepResult(
    end_cause=None,
    grid_cells=((Cell(0, 0),),),
    snake_cells=frozenset({Cell(0, 0)}),
    head=Cell(0, 0),
    tail=Cell(0, 0),
    heading=Direction.right,
    last_turn=Turn.ahead,
    just_ate=False,
    food=None,
)


class ScriptedPlayer:
    # Always goes ahead; counts how often it was asked
    def __init__(self) -> None:
        self.asked_count = 0

    def pick_turn(self, result: StepResult) -> Turn:
        self.asked_count += 1
        return Turn.ahead


def make_player(epsilon: float, min_epsilon: float = 0.0, decay_factor: float = 0.5) -> tuple[ExploringPlayer, ScriptedPlayer]:
    inner = ScriptedPlayer()
    sut = ExploringPlayer(inner, epsilon, min_epsilon, decay_factor, rng=random.Random(0))
    return sut, inner


# ====================  Pick  ====================


def test_zero_epsilon_always_asks_the_inner_player():
    sut, inner = make_player(epsilon=0.0)
    turns = [sut.pick_turn(RESULT) for _ in range(50)]
    assert turns == [Turn.ahead] * 50
    assert inner.asked_count == 50


def test_full_epsilon_never_asks_the_inner_player():
    sut, inner = make_player(epsilon=1.0)
    for _ in range(50):
        sut.pick_turn(RESULT)
    assert inner.asked_count == 0


def test_random_turns_cover_all_three():
    sut, _ = make_player(epsilon=1.0)
    turns = {sut.pick_turn(RESULT) for _ in range(50)}
    assert turns == set(Turn)


# ====================  Decay  ====================


def test_starts_with_the_given_epsilon():
    sut, _ = make_player(epsilon=0.8)
    assert sut.epsilon == 0.8


def test_decay_shrinks_epsilon_by_the_factor():
    sut, _ = make_player(epsilon=0.8, decay_factor=0.5)
    sut.decay_epsilon()
    assert sut.epsilon == pytest.approx(0.4)


def test_decay_stops_at_the_minimum():
    sut, _ = make_player(epsilon=0.8, min_epsilon=0.3, decay_factor=0.5)
    sut.decay_epsilon()
    sut.decay_epsilon()
    assert sut.epsilon == pytest.approx(0.3)
