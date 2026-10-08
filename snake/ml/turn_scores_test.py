import pytest
from snake.core import Turn
from snake.ml.turn_scores import TurnScores


@pytest.mark.parametrize(
    "scores, turn",
    [
        (TurnScores(left=0.9, ahead=0.1, right=0.2), Turn.left),
        (TurnScores(left=0.1, ahead=0.9, right=0.2), Turn.ahead),
        (TurnScores(left=0.1, ahead=0.2, right=0.9), Turn.right),
    ],
)
def test_best_turn_has_the_highest_score(scores, turn):
    assert scores.best_turn == turn


def test_tie_picks_the_first_highest_in_left_ahead_right_order():
    assert TurnScores(left=0.5, ahead=0.5, right=0.1).best_turn == Turn.left
    assert TurnScores(left=0.1, ahead=0.5, right=0.5).best_turn == Turn.ahead
