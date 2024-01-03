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

    async def test_after_interval_invokes_func(self):
        callback = MagicMock()
        sut = Looper(0.01, callback)
        sut.start()
        time.sleep(0.03)
        sut.cancel()
        callback.assert_called()

    async def test_before_first_interval_does_not_invoke_func(self):
        callback = MagicMock()
        sut = Looper(0.01, callback)
        sut.start()
        time.sleep(0.009)
        sut.cancel()
        callback.assert_not_called()

    async def test_passes_args_to_func(self):
        callback = MagicMock()
        arg_int = 1
        arg_str = "something"
        arg_obj = {}
        arg_array = []
        arg_func = lambda: None

        sut = Looper(
            0.01, callback, args=(arg_int, arg_str, arg_obj, arg_array, arg_func)
        )
        sut.start()
        time.sleep(0.03)
        sut.cancel()
        callback.assert_called_with(arg_int, arg_str, arg_obj, arg_array, arg_func)
