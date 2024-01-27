from unittest.mock import MagicMock
from src.game.looper_interval import LooperInterval
from tests.game.helper.counter import Counter
from tests.test_ import Test_async_


class LooperInterval_(Test_async_):
    async def test_when_specified_loops_correct_number_of_times(self):
        counter = Counter()
        sut = LooperInterval(counter.increment, self.msec, self.few)
        await sut.start()
        self.assertEqual(counter.read(), self.few)

    async def test_returns_number_of_times_looped(self):
        counter = Counter()
        sut = LooperInterval(counter.increment, self.msec, self.few)
        actual = await sut.start()
        expected = counter.read()
        self.assertEqual(actual, expected)

    async def test_passes_args_to_func(self):
        cb = MagicMock()

        arg1 = 1
        arg2 = "something"
        arg3 = {}
        arg4 = []
        arg5 = lambda: None

        sut = LooperInterval(
            cb, self.msec, iterations=1, args=(arg1, arg2, arg3, arg4, arg5)
        )
        await sut.start()
        cb.assert_called_with(arg1, arg2, arg3, arg4, arg5)

    async def test_invokes_end_callback(self):
        func = MagicMock()
        end_callback = MagicMock()
        sut = LooperInterval(func, self.msec, self.few, end_callback)
        result = await sut.start()
        end_callback.assert_called_once()
