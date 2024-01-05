import unittest
from unittest.mock import MagicMock
from source.looper import Looper
from test.counter import Counter


class Looper_(unittest.IsolatedAsyncioTestCase):
    _msec = 0.001
    _some_number_1 = 7
    _some_number_2 = 10

    async def test_loops_correct_number_of_times(self):
        counter = Counter()
        sut = Looper(counter.increment, self._msec, self._some_number_1)
        await sut.start()
        self.assertEqual(counter.read(), self._some_number_1)

    async def test_returns_number_of_times_looped(self):
        counter = Counter()
        sut = Looper(counter.increment, self._msec, self._some_number_1)
        actual = await sut.start()
        expected = counter.read()
        self.assertEqual(actual, expected)

    async def test_if_number_of_iterations_unspecified_runs_indefinitely(self):
        # def func():
        #     pass

        # sut = Looper(func, self._msec)
        # await sut.start()
        self.skipTest("Find a way for this")

    async def test_passes_args_to_func(self):
        cb = MagicMock()

        arg1 = 1
        arg2 = "something"
        arg3 = {}
        arg4 = []
        arg5 = lambda: None

        sut = Looper(cb, self._msec, iterations=1, args=(arg1, arg2, arg3, arg4, arg5))
        await sut.start()
        cb.assert_called_with(arg1, arg2, arg3, arg4, arg5)

    async def test_invokes_end_callback(self):
        func = MagicMock()
        end_callback = MagicMock()
        sut = Looper(func, self._msec, self._some_number_1, end_callback)
        result = await sut.start()
        end_callback.assert_called_once()
