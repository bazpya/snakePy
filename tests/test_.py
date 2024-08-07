import tensorflow as tf
from bazpy.testing.testbase_async import TestBaseAsync


class Test_(TestBaseAsync):
    msec = 0.001

    def assertTensorEqual(self, actual: tf.Tensor, expected: tf.Tensor):
        self.assertTrue(tf.math.reduce_all(tf.equal(actual, expected)))

    def assertTensorDifferent(self, actual: tf.Tensor, expected: tf.Tensor):
        self.assertFalse(tf.math.reduce_all(tf.equal(actual, expected)))
