import unittest
from unittest.mock import MagicMock
from source.event import Event


class Event_(unittest.TestCase):
    def test_emit_invokes_callback(self):
        sut = Event()
        callback = MagicMock()
        sut.subscribe(callback)
        sut.emit()
        callback.assert_called()

    def test_emit_passes_args(self):
        sut = Event()
        callback = MagicMock()
        sut.subscribe(callback)
        arg_int = 1
        arg_str = "something"
        arg_obj = {}
        arg_array = []

        arg_func = lambda: None

        sut.emit(arg_int, arg_str, arg_obj, arg_array, arg_func)
        callback.assert_called_with(arg_int, arg_str, arg_obj, arg_array, arg_func)

    def test_unsubscribe_removes_callback(self):
        sut = Event()
        callback = MagicMock()
        sut.subscribe(callback)
        sut.unsubscribe(callback)
        sut.emit()
        callback.assert_not_called()

    def test_purge_removes_all_callbacks(self):
        sut = Event()
        callback1 = MagicMock()
        sut.subscribe(callback1)
        callback2 = MagicMock()
        sut.subscribe(callback2)
        sut.purge()
        sut.emit()
        callback1.assert_not_called()
        callback2.assert_not_called()
