import asyncio
import unittest

from source.looper import Looper


async def bazfunc(seconds: float) -> bool:
    await asyncio.sleep(seconds)
    return True


class Looper_(unittest.IsolatedAsyncioTestCase):
    async def test_an_async_func(self) -> None:
        result = await bazfunc(0.1)
        self.assertTrue(result)
