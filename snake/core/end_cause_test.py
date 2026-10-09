from snake.core.end_cause import EndCause


def test_has_three_causes():
    assert {cause.name for cause in EndCause} == {"crashed", "starved", "won"}
