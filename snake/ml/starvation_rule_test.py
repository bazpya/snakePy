from snake.ml.starvation_rule import StarvationRule


def test_fed_recently_is_not_starved():
    assert StarvationRule(factor=2).is_starved(unfed_step_count=19, grid_cell_count=10) is False


def test_starves_on_reaching_factor_times_the_grid_cell_count():
    assert StarvationRule(factor=2).is_starved(unfed_step_count=20, grid_cell_count=10) is True


def test_limit_grows_with_the_grid():
    sut = StarvationRule(factor=2)
    assert sut.is_starved(unfed_step_count=20, grid_cell_count=10) is True
    assert sut.is_starved(unfed_step_count=20, grid_cell_count=20) is False
