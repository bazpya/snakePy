from snake.core.turn import Turn


def test_has_three_turns():
    assert len(Turn) == 3


def test_values_are_rotation_offsets():
    assert Turn.left.value == -1
    assert Turn.ahead.value == 0
    assert Turn.right.value == 1
