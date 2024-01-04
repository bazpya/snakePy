import unittest
from unittest.mock import MagicMock
from source.looper2 import Looper2


class Looper2_(unittest.IsolatedAsyncioTestCase):
    _msec = 0.001
    _some_number_1 = 7
    _some_number_2 = 10

    async def test_invokes_func(self):
        func = MagicMock()
        sut = Looper2(func, self._msec, 1)
        result = await sut.start()
        func.assert_called()

    async def test_repeates_correct_number_of_times(self):
        func = MagicMock()
        sut = Looper2(func, self._msec, self._some_number_1)
        result = await sut.start()
        self.assertEqual(sut.counter, self._some_number_1)

    async def test_if_iterations_unspecified_runs_indefinitely(self):
        def func(looper: Looper2):
            if looper.counter > self._some_number_2:
                looper.stop()

        sut = Looper2(func, self._msec)
        await sut.start()
        self.assertTrue(True)

    async def test_passes_args_to_func(self):
        cb = MagicMock()

        arg1 = 1
        arg2 = "something"
        arg3 = {}
        arg4 = []
        arg5 = lambda: None

        sut = Looper2(cb, self._msec, iterations=1, args=(arg1, arg2, arg3, arg4, arg5))
        await sut.start()
        cb.assert_called_with(arg1, arg2, arg3, arg4, arg5, sut)
