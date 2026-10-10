from snake.core import Cell, Direction, EndCause, StepResult, Turn
from snake.ml.rewarder import Rewarder


def make_result(just_ate: bool = False, end_cause: EndCause | None = None) -> StepResult:
    # Only just_ate and end_cause matter to the rewarder
    return StepResult(
        end_cause=end_cause,
        grid_cells=((Cell(0, 0), Cell(0, 1)),),
        snake_cells=frozenset({Cell(0, 0)}),
        head=Cell(0, 0),
        tail=Cell(0, 0),
        heading=Direction.right,
        last_turn=Turn.ahead,
        just_ate=just_ate,
        food=None,
    )


def test_plain_step_gives_nothing():
    assert Rewarder().get_reward(make_result()) == 0


def test_eating_is_rewarded():
    assert Rewarder().get_reward(make_result(just_ate=True)) == 1


def test_crashing_is_punished():
    assert Rewarder().get_reward(make_result(end_cause=EndCause.crashed)) == -1


def test_filling_the_grid_is_rewarded():
    # The last bite fills the grid: a win
    assert Rewarder().get_reward(make_result(just_ate=True, end_cause=EndCause.won)) == 1


def test_starving_is_punished():
    assert Rewarder().get_reward(make_result(end_cause=EndCause.starved)) == -1
