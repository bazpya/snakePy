import pytest
from snake.core import Factory, Turn
from snake.ml.eye import Eye
from snake.ml.brain import Brain
from snake.ml.turn_estimates import TurnEstimates

SIGHT = [0.1, 0.2, 0.3]


def test_estimates_each_turn():
    sut = Brain(input_count=3)
    assert isinstance(sut.estimate(SIGHT), TurnEstimates)


def test_same_sight_gives_same_estimates():
    sut = Brain(input_count=3)
    assert sut.estimate(SIGHT) == sut.estimate(SIGHT)


def test_wrong_sized_sight_is_rejected():
    sut = Brain(input_count=3)
    with pytest.raises(ValueError):
        sut.estimate([0.1, 0.2])


def test_estimates_what_the_eye_sees():
    eye = Eye()
    result = Factory(row_count=5, col_count=5).create().initial_result
    sut = Brain(input_count=eye.output_count)
    assert isinstance(sut.estimate(eye.see(result)), TurnEstimates)


# ====================  Learn  ====================


def learn_repeatedly(sut: Brain, turn: Turn, target: float, count: int = 300) -> list[float]:
    # Learns from one sight over and over; returns the losses
    return [sut.learn([SIGHT], [turn], [target]) for _ in range(count)]


def test_learning_moves_the_estimate_towards_the_target():
    sut = Brain(input_count=3, learning_rate=0.01)
    learn_repeatedly(sut, Turn.left, target=5.0)
    assert sut.estimate(SIGHT).left == pytest.approx(5.0, abs=0.1)


def test_learning_only_aims_at_the_chosen_turn():
    sut = Brain(input_count=3, learning_rate=0.01)
    learn_repeatedly(sut, Turn.right, target=5.0)
    assert sut.estimate(SIGHT).right == pytest.approx(5.0, abs=0.1)
    assert sut.estimate(SIGHT).left != pytest.approx(5.0, abs=0.1)


def test_learning_reports_a_shrinking_loss():
    sut = Brain(input_count=3, learning_rate=0.01)
    losses = learn_repeatedly(sut, Turn.ahead, target=5.0)
    assert losses[-1] < losses[0]


def test_learning_rejects_mismatched_batches():
    sut = Brain(input_count=3)
    with pytest.raises(ValueError):
        sut.learn([SIGHT, SIGHT], [Turn.left], [1.0])


# ====================  Copy  ====================


def test_copy_gives_the_same_estimates():
    sut = Brain(input_count=3)
    assert sut.copy().estimate(SIGHT) == sut.estimate(SIGHT)


def test_copy_is_unaffected_by_later_learning():
    sut = Brain(input_count=3, learning_rate=0.01)
    copy = sut.copy()
    before = copy.estimate(SIGHT)
    learn_repeatedly(sut, Turn.left, target=5.0, count=10)
    assert copy.estimate(SIGHT) == before
    assert sut.estimate(SIGHT) != before


# ====================  Save  ====================


def test_loaded_brain_gives_the_same_estimates(tmp_path):
    path = tmp_path / "brain.pt"
    saved = Brain(input_count=3)
    saved.save(path)
    sut = Brain(input_count=3)
    sut.load(path)
    assert sut.estimate(SIGHT) == saved.estimate(SIGHT)


def test_loaded_brain_still_learns(tmp_path):
    path = tmp_path / "brain.pt"
    Brain(input_count=3).save(path)
    sut = Brain(input_count=3, learning_rate=0.01)
    sut.load(path)
    losses = learn_repeatedly(sut, Turn.ahead, target=5.0)
    assert losses[-1] < losses[0]


def test_loading_a_different_sized_brain_is_rejected(tmp_path):
    path = tmp_path / "brain.pt"
    Brain(input_count=4).save(path)
    sut = Brain(input_count=3)
    with pytest.raises(ValueError):
        sut.load(path)
