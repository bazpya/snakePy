from snake.core import Cell, Direction, StepResult, Turn
from snake.human.human_player import HumanPlayer


def make_result(heading: Direction) -> StepResult:
    # Only the heading matters to the player
    return StepResult(
        end_cause=None,
        grid_cells=((Cell(0, 0),),),
        snake_cells=frozenset({Cell(0, 0)}),
        head=Cell(0, 0),
        heading=heading,
        last_turn=Turn.ahead,
        just_ate=False,
        food=None,
    )


RIGHT = make_result(Direction.right)
UP = make_result(Direction.up)
LEFT = make_result(Direction.left)


class FakeKeySource:
    # Delivers keys on demand, instead of from a real keyboard
    def __init__(self) -> None:
        self.listeners: list = []

    def add_listener(self, listener) -> None:
        self.listeners.append(listener)

    def press(self, key: str) -> None:
        for listener in self.listeners:
            listener(key)


def make_player(*keys: str) -> HumanPlayer:
    key_source = FakeKeySource()
    sut = HumanPlayer(key_source)
    for key in keys:
        key_source.press(key)
    return sut


# ====================  Key source  ====================


def test_listens_to_its_key_source():
    key_source = FakeKeySource()
    HumanPlayer(key_source)
    assert len(key_source.listeners) == 1


# ====================  Translate  ====================


def test_empty_queue_goes_ahead():
    sut = make_player()
    assert sut.pick_turn(RIGHT) == Turn.ahead


def test_key_to_the_left_turns_left():
    sut = make_player("Up")
    assert sut.pick_turn(RIGHT) == Turn.left


def test_key_to_the_right_turns_right():
    sut = make_player("Down")
    assert sut.pick_turn(RIGHT) == Turn.right


def test_key_in_the_same_direction_goes_ahead():
    sut = make_player("Right")
    assert sut.pick_turn(RIGHT) == Turn.ahead


def test_reverse_key_goes_ahead():
    sut = make_player("Left")
    assert sut.pick_turn(RIGHT) == Turn.ahead


def test_unknown_key_is_ignored():
    sut = make_player("a")
    assert sut.pick_turn(RIGHT) == Turn.ahead


# ====================  Queue  ====================


def test_keys_come_out_one_per_call_in_press_order():
    sut = make_player("Up", "Left")
    assert sut.pick_turn(RIGHT) == Turn.left
    assert sut.pick_turn(UP) == Turn.left


def test_drained_queue_goes_ahead():
    sut = make_player("Up")
    sut.pick_turn(RIGHT)
    assert sut.pick_turn(UP) == Turn.ahead


def test_repeated_key_is_queued_once():
    # Without collapsing, the second Up would give ahead
    sut = make_player("Up", "Up", "Left")
    assert sut.pick_turn(RIGHT) == Turn.left
    assert sut.pick_turn(UP) == Turn.left


def test_only_back_to_back_repeats_collapse():
    sut = make_player("Up", "Left", "Up")
    assert sut.pick_turn(RIGHT) == Turn.left
    assert sut.pick_turn(UP) == Turn.left
    assert sut.pick_turn(LEFT) == Turn.right


def test_keys_beyond_the_cap_are_dropped():
    # 10 alternating keys fill the queue; the 11th (Up) would turn left
    sut = make_player(*["Up", "Down"] * 5, "Up")
    for _ in range(10):
        sut.pick_turn(RIGHT)
    assert sut.pick_turn(RIGHT) == Turn.ahead
