import asyncio
import time
import unittest
from unittest.mock import MagicMock
from source.looper import Looper


async def bazfunc(seconds: float) -> bool:
    await asyncio.sleep(seconds)
    return True


class Looper_(unittest.IsolatedAsyncioTestCase):
    async def test_an_async_func(self):
        result = await bazfunc(0.01)
        self.assertTrue(result)

    def test_after_interval_invokes_func(self):
        callback = MagicMock()
        sut = Looper(0.01, callback)
        sut.start()
        time.sleep(0.03)
        sut.cancel()
        callback.assert_called()

    def test_before_first_interval_does_not_invoke_func(self):
        callback = MagicMock()
        sut = Looper(0.01, callback)
        sut.start()
        time.sleep(0.009)
        sut.cancel()
        callback.assert_not_called()

    def test_passes_args_to_func(self):
        cb = MagicMock()
        arg1 = 1
        arg2 = "something"
        arg3 = {}
        arg4 = []
        arg5 = lambda: None

        sut = Looper(0.01, cb, args=(arg1, arg2, arg3, arg4, arg5))
        sut.start()
        time.sleep(0.03)
        sut.cancel()
        cb.assert_called_with(sut, arg1, arg2, arg3, arg4, arg5)

    def test_invokes_func_repeatedly(self):
        def cb(looper):  # todo: make awaitable
            looper.counter = looper.counter + 1
            if looper.counter == 3:
                looper.cancel()

        sut = Looper(0.001, cb)
        sut.start()
        time.sleep(0.05)
        self.assertEqual(3, sut.counter)
