import unittest


class Test_base_:
    few = 7
    some = 10
    many = 20
    msec = 0.001


class Test_(Test_base_, unittest.TestCase):
    pass


class Test_async_(Test_base_, unittest.IsolatedAsyncioTestCase):
    pass
