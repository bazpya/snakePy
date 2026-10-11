from snake.ui.clock import Clock

INTERVAL_MS = 120


class FakeTime:
    # A time source the test moves by hand, in milliseconds
    def __init__(self) -> None:
        self.now_ms = 1000.0  # not zero, so the start time matters

    def __call__(self) -> float:
        return self.now_ms


def make_started_clock() -> tuple[Clock, FakeTime]:
    time = FakeTime()
    sut = Clock(INTERVAL_MS, time)
    sut.start()
    return sut, time


# ====================  Wait  ====================


def test_first_wait_is_one_interval():
    sut, _ = make_started_clock()
    assert sut.get_wait_ms() == 120


def test_passing_time_shortens_the_wait():
    sut, time = make_started_clock()
    time.now_ms += 30
    assert sut.get_wait_ms() == 90


def test_wait_is_never_negative():
    sut, time = make_started_clock()
    time.now_ms += 200
    assert sut.get_wait_ms() == 0


def test_wait_is_whole_milliseconds():
    sut, time = make_started_clock()
    time.now_ms += 30.4
    assert isinstance(sut.get_wait_ms(), int)


# ====================  Beat  ====================


def test_a_slow_step_eats_into_the_next_wait():
    sut, time = make_started_clock()
    time.now_ms += 120  # the first tick is due
    sut.advance()
    time.now_ms += 50  # the step took 50 ms
    assert sut.get_wait_ms() == 70


def test_beat_stays_fixed_over_many_ticks():
    sut, time = make_started_clock()
    start_ms = time.now_ms
    for step_ms in (10, 60, 25, 90, 5, 45):  # uneven step durations
        time.now_ms += sut.get_wait_ms()  # wait until due
        time.now_ms += step_ms  # do the step
        sut.advance()
    # Six ticks done: the seventh is due exactly seven intervals after the start
    assert time.now_ms + sut.get_wait_ms() == start_ms + 7 * INTERVAL_MS


def test_falling_far_behind_skips_to_the_next_beat_without_a_burst():
    sut, time = make_started_clock()
    start_ms = time.now_ms
    time.now_ms = start_ms + 500  # stalled: the tick due at +120 fires late
    sut.advance()
    # Beats fall at +120, +240, +360, +480, +600: the next one ahead is +600
    assert sut.get_wait_ms() == 100
