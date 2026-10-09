from snake.core import Cell, Direction, StepResult, Turn
from snake.ml.stats import Stats


def make_result(just_ate: bool = False) -> StepResult:
    # Only just_ate matters to Stats
    return StepResult(
        is_over=False,
        grid_cells=((Cell(0, 0), Cell(0, 1)),),
        snake_cells=frozenset({Cell(0, 0)}),
        head=Cell(0, 0),
        heading=Direction.right,
        last_turn=Turn.ahead,
        just_ate=just_ate,
        food=None,
    )


def make_started_stats() -> Stats:
    sut = Stats()
    sut.on_started(make_result())
    return sut


# ====================  Start  ====================


def test_start_counts_from_zero():
    sut = make_started_stats()
    assert sut.taken_step_count == 0
    assert sut.unfed_step_count == 0


def test_start_resets_for_a_new_game():
    sut = make_started_stats()
    sut.on_stepped(make_result())
    sut.on_started(make_result())
    assert sut.taken_step_count == 0
    assert sut.unfed_step_count == 0


# ====================  Step  ====================


def test_each_step_is_counted():
    sut = make_started_stats()
    sut.on_stepped(make_result())
    sut.on_stepped(make_result(just_ate=True))
    assert sut.taken_step_count == 2


def test_steps_without_food_are_counted():
    sut = make_started_stats()
    sut.on_stepped(make_result())
    sut.on_stepped(make_result())
    assert sut.unfed_step_count == 2


def test_eating_resets_the_unfed_count():
    sut = make_started_stats()
    sut.on_stepped(make_result())
    sut.on_stepped(make_result(just_ate=True))
    assert sut.unfed_step_count == 0
