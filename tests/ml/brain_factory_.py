from src.ml.ml import ML
from tests.test_ import Test_
from src.ml.brain_factory import BrainFactory


class Brain_factory_(Test_):
    def test_makes_correct_type_of_model(self):
        res = BrainFactory.make(self.some, self.few)
        self.assertIsInstance(res, ML.keras.Sequential)

    def test_makes_correct_number_of_layers(self):
        res = BrainFactory.make(self.some, self.few)
        expected = len(BrainFactory.spec.layer_sizes) + 1
        actual = len(res.layers)
        self.assertEqual(actual, expected)

    def test_makes_correct_layer_sizes(self):
        res = BrainFactory.make(self.some, self.few)
        for i, size in enumerate(BrainFactory.spec.layer_sizes):
            layer = res.layers[i]
            self.assertEqual(layer.units, size)

    def test_makes_correct_output_layer_size(self):
        res = BrainFactory.make(self.some, self.few)
        last_layer = res.layers[-1]
        actual = last_layer.units
        expected = self.few
        self.assertEqual(actual, expected)

    # ======================

    def test_clone_makes_correct_type_of_model(self):
        original = BrainFactory.make(self.some, self.few)
        clone = BrainFactory.clone(original)
        self.assertIsInstance(clone, ML.keras.Sequential)

    def test_clone_makes_correct_number_of_layers(self):
        original = BrainFactory.make(self.some, self.few)
        clone = BrainFactory.clone(original)
        expected = len(original.layers)
        actual = len(clone.layers)
        self.assertEqual(actual, expected)

    def test_clone_makes_correct_layer_sizes(self):
        original = BrainFactory.make(self.some, self.few)
        clone = BrainFactory.clone(original)
        for i, size in enumerate(BrainFactory.spec.layer_sizes):
            layer = clone.layers[i]
            self.assertEqual(layer.units, size)

    def test_clone_makes_correct_output_layer_size(self):
        original = BrainFactory.make(self.some, self.few)
        clone = BrainFactory.clone(original)
        last_layer = clone.layers[-1]
        actual = last_layer.units
        expected = self.few
        self.assertEqual(actual, expected)

    def test_clone_makes_correct_weights(self):
        original = BrainFactory.make(self.some, self.few)
        clone = BrainFactory.clone(original)
        for ind, size in enumerate(BrainFactory.spec.layer_sizes):
            original_weights = original.layers[ind].get_weights()
            clone_weights = clone.layers[ind].get_weights()
            self.assertTensorEqual(original_weights, clone_weights)
