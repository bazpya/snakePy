from snake.core import Cell, Direction, StepResult, Turn
from snake.ml.stats import Stats


def make_result() -> StepResult:
    return StepResult(
        end_cause=None,
        grid_cells=((Cell(0, 0), Cell(0, 1)),),
        snake_cells=frozenset({Cell(0, 0)}),
        head=Cell(0, 0),
        heading=Direction.right,
        last_turn=Turn.ahead,
        just_ate=False,
        food=None,
    )


def make_started_stats() -> Stats:
    sut = Stats()
    sut.on_started(make_result())
    return sut


def test_start_counts_from_zero():
    assert make_started_stats().taken_step_count == 0


def test_start_resets_for_a_new_game():
    sut = make_started_stats()
    sut.on_stepped(make_result())
    sut.on_started(make_result())
    assert sut.taken_step_count == 0


def test_each_step_is_counted():
    sut = make_started_stats()
    sut.on_stepped(make_result())
    sut.on_stepped(make_result())
    assert sut.taken_step_count == 2
