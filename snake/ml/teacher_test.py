import pytest
from snake.core import Turn
from snake.ml.experience import Experience
from snake.ml.teacher import Teacher
from snake.ml.turn_estimates import TurnEstimates

DISCOUNT = 0.9


def make_experience(reward: float = 1.0, is_over: bool = False, turn: Turn = Turn.ahead) -> Experience:
    return Experience(state=[0.1], turn=turn, reward=reward, next_state=[0.2], is_over=is_over)


class FakeLearner:
    # Every state looks the same: best_estimate is the highest; records what it was taught
    def __init__(self, best_estimate: float = 2.0) -> None:
        self.best_estimate = best_estimate
        self.lessons: list[tuple[list[list[float]], list[Turn], list[float]]] = []

    def estimate(self, state: list[float]) -> TurnEstimates:
        return TurnEstimates(left=0.0, ahead=self.best_estimate, right=0.0)

    def learn(self, states: list[list[float]], turns: list[Turn], targets: list[float]) -> float:
        self.lessons.append((states, turns, targets))
        return 0.5

    def copy(self) -> "FakeLearner":
        return FakeLearner(self.best_estimate)


class FakeMemory:
    # Hands out the first experiences, so tests can predict the batch
    def __init__(self, *experiences: Experience) -> None:
        self._experiences = list(experiences)

    @property
    def size(self) -> int:
        return len(self._experiences)

    def sample(self, count: int) -> list[Experience]:
        return self._experiences[:count]


def make_teacher(*experiences: Experience, batch_size: int = 1) -> tuple[Teacher, FakeLearner]:
    learner = FakeLearner()
    sut = Teacher(learner, FakeMemory(*experiences), batch_size, DISCOUNT)
    return sut, learner


def get_targets(learner: FakeLearner) -> list[float]:
    _, _, targets = learner.lessons[-1]
    return targets


# ====================  Batch  ====================


def test_too_few_experiences_teaches_nothing():
    sut, learner = make_teacher(make_experience(), batch_size=2)
    assert sut.teach() is None
    assert learner.lessons == []


def test_teaches_one_batch_of_the_given_size():
    sut, learner = make_teacher(make_experience(), make_experience(), make_experience(), batch_size=2)
    sut.teach()
    states, turns, targets = learner.lessons[0]
    assert len(states) == len(turns) == len(targets) == 2


def test_passes_on_the_states_and_turns():
    sut, learner = make_teacher(make_experience(turn=Turn.left))
    sut.teach()
    states, turns, _ = learner.lessons[0]
    assert states == [[0.1]]
    assert turns == [Turn.left]


def test_returns_the_loss():
    sut, _ = make_teacher(make_experience())
    assert sut.teach() == 0.5


# ====================  Target  ====================


def test_target_adds_the_discounted_best_estimate_of_the_next_state():
    sut, learner = make_teacher(make_experience(reward=1.0))
    sut.teach()
    assert get_targets(learner) == [pytest.approx(1.0 + DISCOUNT * 2.0)]


def test_target_is_only_the_reward_when_the_game_is_over():
    sut, learner = make_teacher(make_experience(reward=-1.0, is_over=True))
    sut.teach()
    assert get_targets(learner) == [-1.0]


def test_target_copy_stays_fixed_until_synced():
    sut, learner = make_teacher(make_experience(reward=0.0))
    learner.best_estimate = 10.0  # the learner moves on
    sut.teach()
    assert get_targets(learner) == [pytest.approx(DISCOUNT * 2.0)]
    sut.sync_target()
    sut.teach()
    assert get_targets(learner) == [pytest.approx(DISCOUNT * 10.0)]
