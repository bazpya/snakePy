from snake.core import Cell, Direction, StepResult, Turn
from snake.ml.rewarder import Rewarder


def make_result(just_ate: bool = False, is_over: bool = False) -> StepResult:
    # Only just_ate and is_over matter to the rewarder
    return StepResult(
        is_over=is_over,
        grid_cells=((Cell(0, 0), Cell(0, 1)),),
        snake_cells=frozenset({Cell(0, 0)}),
        head=Cell(0, 0),
        heading=Direction.right,
        last_turn=Turn.ahead,
        just_ate=just_ate,
        food=None,
    )


def test_plain_step_gives_nothing():
    assert Rewarder().get_reward(make_result(), is_starved=False) == 0


def test_eating_is_rewarded():
    assert Rewarder().get_reward(make_result(just_ate=True), is_starved=False) == 1


def test_crashing_is_punished():
    assert Rewarder().get_reward(make_result(is_over=True), is_starved=False) == -1


def test_filling_the_grid_is_rewarded():
    # Over, but the snake ate: a win, not a crash
    assert Rewarder().get_reward(make_result(just_ate=True, is_over=True), is_starved=False) == 1


def test_starving_is_punished():
    # The training loop cut the game short: too long without food
    assert Rewarder().get_reward(make_result(), is_starved=True) == -1
