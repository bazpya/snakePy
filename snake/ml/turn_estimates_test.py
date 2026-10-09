import pytest
from snake.core import Turn
from snake.ml.turn_estimates import TurnEstimates


@pytest.mark.parametrize(
    "estimates, turn",
    [
        (TurnEstimates(left=0.9, ahead=0.1, right=0.2), Turn.left),
        (TurnEstimates(left=0.1, ahead=0.9, right=0.2), Turn.ahead),
        (TurnEstimates(left=0.1, ahead=0.2, right=0.9), Turn.right),
    ],
)
def test_best_turn_has_the_highest_estimate(estimates, turn):
    assert estimates.best_turn == turn


def test_tie_picks_the_first_highest_in_left_ahead_right_order():
    assert TurnEstimates(left=0.5, ahead=0.5, right=0.1).best_turn == Turn.left
    assert TurnEstimates(left=0.1, ahead=0.5, right=0.5).best_turn == Turn.ahead


def test_best_estimate_is_the_highest_value():
    assert TurnEstimates(left=0.1, ahead=0.7, right=0.3).best_estimate == 0.7
