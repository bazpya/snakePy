from snake.core import Cell, Direction, StepResult, Turn
from snake.ml.rewarder import Rewarder


def make_result(snake_length: int, is_over: bool = False) -> StepResult:
    # Only the snake's length and is_over matter to the rewarder
    snake_cells = [Cell(0, col) for col in range(snake_length)]
    return StepResult(
        is_over=is_over,
        grid_cells=(tuple(Cell(0, col) for col in range(5)),),
        snake_cells=frozenset(snake_cells),
        head=snake_cells[-1],
        heading=Direction.right,
        last_turn=Turn.ahead,
        just_ate=False,
        food=None,
    )


def test_plain_step_gives_nothing():
    assert Rewarder().get_reward(make_result(2), make_result(2)) == 0


def test_eating_is_rewarded():
    assert Rewarder().get_reward(make_result(2), make_result(3)) == 1


def test_crashing_is_punished():
    assert Rewarder().get_reward(make_result(2), make_result(2, is_over=True)) == -1


def test_filling_the_grid_is_rewarded():
    # Over, but the snake grew: a win, not a crash
    assert Rewarder().get_reward(make_result(4), make_result(5, is_over=True)) == 1


def test_starving_is_punished():
    # The training loop cut the game short: too long without food
    assert Rewarder().get_reward(make_result(2), make_result(2), is_starved=True) == -1
