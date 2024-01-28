import unittest


class Test_base_(unittest.TestCase):
    few = 7
    some = 10
    many = 20
    msec = 0.001

    def assertListLength(self, list: list, length: int):
        self.assertEqual(len(list), length)

    def assertListEmpty(self, list: list):
        self.assertListLength(list, 0)


class Test_(Test_base_, unittest.TestCase):
    pass


class Test_async_(Test_base_, unittest.IsolatedAsyncioTestCase):
    pass
