import unittest
from unittest.mock import MagicMock
from source.looper_sync import LooperSync
from test.helper.counter import Counter


class LooperSync_(unittest.TestCase):
    _some_number_1 = 7
    _some_number_2 = 10

    def test_when_specified_loops_correct_number_of_times(self):
        counter = Counter()
        sut = LooperSync(counter.increment, self._some_number_1)
        sut.start()
        self.assertEqual(counter.read(), self._some_number_1)

    def test_returns_number_of_times_looped(self):
        counter = Counter()
        sut = LooperSync(counter.increment, self._some_number_1)
        actual = sut.start()
        expected = counter.read()
        self.assertEqual(actual, expected)

    def test_if_unspecified_runs_indefinitely(self):
        self.skipTest("todo")

    def test_passes_args_to_func(self):
        cb = MagicMock()

        arg1 = 1
        arg2 = "something"
        arg3 = {}
        arg4 = []
        arg5 = lambda: None

        sut = LooperSync(
            cb, iterations=1, args=(arg1, arg2, arg3, arg4, arg5)
        )
        sut.start()
        cb.assert_called_with(arg1, arg2, arg3, arg4, arg5)

    def test_invokes_end_callback(self):
        func = MagicMock()
        end_callback = MagicMock()
        sut = LooperSync(func, self._some_number_1, end_callback)
        result = sut.start()
        end_callback.assert_called_once()
