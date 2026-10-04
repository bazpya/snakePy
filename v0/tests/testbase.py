from bazpy.testing.testbase_async import TestBaseAsync
from src.ml.ml import ML


class Test_(TestBaseAsync):
    msec = 0.001

    def assertTensorEqual(self, actual: ML.Tensor, expected: ML.Tensor):
        self.assertTrue(ML.math.reduce_all(ML.equal(actual, expected)))

    def assertTensorDifferent(self, actual: ML.Tensor, expected: ML.Tensor):
        self.assertFalse(ML.math.reduce_all(ML.equal(actual, expected)))
