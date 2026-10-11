from snake.core import Cell, Direction, EndCause, Turn, WorldState
from snake.ml.experience import Experience
from snake.ml.recorder import Recorder
from snake.ml.rewarder import Rewarder


def make_state(
    col: int,
    last_turn: Turn = Turn.ahead,
    just_ate: bool = False,
    end_cause: EndCause | None = None,
) -> WorldState:
    # The head's column tells states apart
    return WorldState(
        end_cause=end_cause,
        grid_cells=(tuple(Cell(0, c) for c in range(5)),),
        snake_cells=frozenset({Cell(0, col)}),
        head=Cell(0, col),
        tail=Cell(0, col),
        heading=Direction.right,
        last_turn=last_turn,
        just_ate=just_ate,
        food=None,
    )


class ColumnEye:
    # Sees only the head's column, so sights are easy to tell apart
    def see(self, state: WorldState) -> list[float]:
        return [float(state.head.col)]


class RecordingMemory:
    # Keeps what was added, in order
    def __init__(self) -> None:
        self.experiences: list[Experience] = []

    def add(self, experience: Experience) -> None:
        self.experiences.append(experience)


def make_started_recorder() -> tuple[Recorder, RecordingMemory]:
    memory = RecordingMemory()
    sut = Recorder(ColumnEye(), Rewarder(), memory)
    sut.on_started(make_state(0))
    return sut, memory


# ====================  Start  ====================


def test_start_records_nothing():
    _, memory = make_started_recorder()
    assert memory.experiences == []


# ====================  Step  ====================


def test_each_step_adds_one_experience():
    sut, memory = make_started_recorder()
    sut.on_stepped(make_state(1))
    sut.on_stepped(make_state(2))
    assert len(memory.experiences) == 2


def test_experience_holds_what_was_seen_before_and_after():
    sut, memory = make_started_recorder()
    sut.on_stepped(make_state(1))
    assert memory.experiences[0].sight == [0.0]
    assert memory.experiences[0].next_sight == [1.0]


def test_experience_holds_the_turn_taken():
    sut, memory = make_started_recorder()
    sut.on_stepped(make_state(1, last_turn=Turn.left))
    assert memory.experiences[0].turn == Turn.left


def test_experience_holds_the_reward():
    sut, memory = make_started_recorder()
    sut.on_stepped(make_state(1, just_ate=True))
    assert memory.experiences[0].reward == 1.0


def test_experience_is_not_over_while_the_game_goes_on():
    sut, memory = make_started_recorder()
    sut.on_stepped(make_state(1))
    assert memory.experiences[0].is_over is False


def test_experience_is_over_when_the_game_ends():
    sut, memory = make_started_recorder()
    sut.on_stepped(make_state(1, end_cause=EndCause.starved))
    assert memory.experiences[0].is_over is True


def test_next_sight_becomes_the_following_sight():
    sut, memory = make_started_recorder()
    sut.on_stepped(make_state(1))
    sut.on_stepped(make_state(2))
    assert memory.experiences[1].sight == [1.0]
    assert memory.experiences[1].next_sight == [2.0]


def test_new_game_starts_from_a_fresh_sight():
    sut, memory = make_started_recorder()
    sut.on_stepped(make_state(1, end_cause=EndCause.crashed))
    sut.on_started(make_state(3))
    sut.on_stepped(make_state(4))
    assert memory.experiences[1].sight == [3.0]
