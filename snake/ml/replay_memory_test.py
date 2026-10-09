import random
import pytest
from snake.core import Turn
from snake.ml.experience import Experience
from snake.ml.replay_memory import ReplayMemory


def make_experience(number: int) -> Experience:
    # The reward tells experiences apart
    return Experience(
        state=[0.0],
        turn=Turn.ahead,
        reward=float(number),
        next_state=[0.0],
        is_over=False,
    )


def make_memory(capacity: int, added_count: int, rng: random.Random | None = None) -> ReplayMemory:
    sut = ReplayMemory(capacity, rng)
    for number in range(added_count):
        sut.add(make_experience(number))
    return sut


def get_rewards(experiences: list[Experience]) -> set[float]:
    return {experience.reward for experience in experiences}


def test_new_memory_is_empty():
    assert ReplayMemory(capacity=3).size == 0


def test_adding_grows_the_size():
    assert make_memory(capacity=3, added_count=2).size == 2


def test_full_memory_drops_the_oldest():
    sut = make_memory(capacity=3, added_count=4)
    assert sut.size == 3
    assert get_rewards(sut.sample(3)) == {1.0, 2.0, 3.0}


def test_sample_gives_the_asked_count_from_what_was_added():
    sut = make_memory(capacity=10, added_count=5)
    sample = sut.sample(3)
    assert len(sample) == 3
    assert get_rewards(sample) <= {0.0, 1.0, 2.0, 3.0, 4.0}


def test_sampling_more_than_held_is_rejected():
    sut = make_memory(capacity=10, added_count=2)
    with pytest.raises(ValueError):
        sut.sample(3)


def test_seeded_sampling_repeats():
    first = make_memory(capacity=10, added_count=5, rng=random.Random(1))
    second = make_memory(capacity=10, added_count=5, rng=random.Random(1))
    assert first.sample(3) == second.sample(3)
