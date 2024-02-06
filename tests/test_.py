import unittest
import tensorflow as tf


class Test_(unittest.IsolatedAsyncioTestCase):
    few = 7
    some = 10
    many = 20
    msec = 0.001

    def make_getter(self, x):
        return lambda *args, **kwargs: x

    def assertListLength(self, list: list, length: int):
        self.assertEqual(len(list), length)

    def assertListEmpty(self, list: list):
        self.assertListLength(list, 0)

    def assertZero(self, value):
        self.assertEqual(value, 0)

    def assertTensorEqual(self, actual: tf.Tensor, expected: tf.Tensor):
        self.assertTrue(tf.math.reduce_all(tf.equal(actual, expected)))

    def assertTensorDifferent(self, actual: tf.Tensor, expected: tf.Tensor):
        self.assertFalse(tf.math.reduce_all(tf.equal(actual, expected)))
