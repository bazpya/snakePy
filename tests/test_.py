import unittest


class Test_(unittest.IsolatedAsyncioTestCase):
    few = 7
    some = 10
    many = 20
    msec = 0.001

    def assertListLength(self, list: list, length: int):
        self.assertEqual(len(list), length)

    def assertListEmpty(self, list: list):
        self.assertListLength(list, 0)
