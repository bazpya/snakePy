import pytest
from snake.core import Factory
from snake.ml.eye import Eye
from snake.ml.brain import Brain
from snake.ml.turn_estimates import TurnEstimates

STATE = [0.1, 0.2, 0.3]


def test_estimates_each_turn():
    sut = Brain(input_count=3)
    assert isinstance(sut.estimate(STATE), TurnEstimates)


def test_same_state_gives_same_estimates():
    sut = Brain(input_count=3)
    assert sut.estimate(STATE) == sut.estimate(STATE)


def test_wrong_sized_state_is_rejected():
    sut = Brain(input_count=3)
    with pytest.raises(ValueError):
        sut.estimate([0.1, 0.2])


def test_estimates_what_the_eye_sees():
    eye = Eye()
    result = Factory(row_count=5, col_count=5).create().initial_result
    sut = Brain(input_count=eye.output_count)
    assert isinstance(sut.estimate(eye.see(result)), TurnEstimates)
