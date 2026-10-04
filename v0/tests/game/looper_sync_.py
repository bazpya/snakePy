from tests.testbase import Test_
from unittest.mock import MagicMock
from src.game.looper_sync import LooperSync
from tests.game.helper.counter import Counter


class LooperSync_(Test_):
    _counter: Counter

    def setUp(self):
        self._counter = Counter()

    def test_when_specified_iterates_correct_number_of_times(self):
        sut = LooperSync(self._counter.increment, self.few)
        sut.start()
        self.assertEqual(self._counter.read(), self.few)

    def test_when_unspecified_iterations_runs_indefinitely(self):
        expected = self.many

        def step_func():
            self._counter.increment()
            if self._counter.read() == expected:
                sut.stop()

        sut = LooperSync(step_func)
        sut.start()
        actual = self._counter.read()
        self.assertEqual(actual, expected)

    def test_returns_number_of_times_looped(self):
        sut = LooperSync(self._counter.increment, self.few)
        actual = sut.start()
        expected = self._counter.read()
        self.assertEqual(actual, expected)

    def test_passes_args_to_func(self):
        cb = MagicMock()

        arg1 = 1
        arg2 = "something"
        arg3 = {}
        arg4 = []
        arg5 = lambda: None

        sut = LooperSync(cb, iterations=1, args=(arg1, arg2, arg3, arg4, arg5))
        sut.start()
        cb.assert_called_with(arg1, arg2, arg3, arg4, arg5)

    def test_invokes_end_callback(self):
        func = MagicMock()
        end_cb = MagicMock()
        sut = LooperSync(func, self.few, end_callback=end_cb)
        result = sut.start()
        end_cb.assert_called_once()
