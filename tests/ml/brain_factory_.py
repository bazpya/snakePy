import os
from src.ml.ml import ML
from src.config import config
from tests.test_ import Test_
from src.ml.brain_factory import BrainFactory as BF


class Brain_factory_(Test_):
    _dir = config.ml.brain.save_dir

    def test_makes_correct_type_of_model(self):
        res = BF.make(self.some, self.few)
        self.assertIsInstance(res, ML.keras.Sequential)

    def test_makes_correct_number_of_layers(self):
        res = BF.make(self.some, self.few)
        expected = len(BF.spec.layer_sizes) + 1
        actual = len(res.layers)
        self.assertEqual(actual, expected)

    def test_makes_correct_layer_sizes(self):
        res = BF.make(self.some, self.few)
        for i, size in enumerate(BF.spec.layer_sizes):
            layer = res.layers[i]
            self.assertEqual(layer.units, size)

    def test_makes_correct_output_layer_size(self):
        res = BF.make(self.some, self.few)
        last_layer = res.layers[-1]
        actual = last_layer.units
        expected = self.few
        self.assertEqual(actual, expected)

    # ======================  Cloning  ======================

    def test_clone_makes_correct_type_of_model(self):
        original = BF.make(self.some, self.few)
        clone = BF.clone(original)
        self.assertIsInstance(clone, ML.keras.Sequential)

    def test_clone_makes_correct_number_of_layers(self):
        original = BF.make(self.some, self.few)
        clone = BF.clone(original)
        expected = len(original.layers)
        actual = len(clone.layers)
        self.assertEqual(actual, expected)

    def test_clone_makes_correct_layer_sizes(self):
        original = BF.make(self.some, self.few)
        clone = BF.clone(original)
        for i, size in enumerate(BF.spec.layer_sizes):
            layer = clone.layers[i]
            self.assertEqual(layer.units, size)

    def test_clone_makes_correct_output_layer_size(self):
        original = BF.make(self.some, self.few)
        clone = BF.clone(original)
        last_layer = clone.layers[-1]
        actual = last_layer.units
        expected = self.few
        self.assertEqual(actual, expected)

    def test_clone_makes_correct_weights(self):
        original = BF.make(self.some, self.few)
        clone = BF.clone(original)
        for ind, size in enumerate(BF.spec.layer_sizes):
            original_weights = original.layers[ind].get_weights()
            clone_weights = clone.layers[ind].get_weights()
            self.assertTensorEqual(original_weights, clone_weights)

    # ======================  Saving/Loading  ======================

    def test_load(self):
        filename = config.ml.brain.ancestor_example_name
        brain = BF.load(filename)
        self.assertIsInstance(brain, ML.keras.Sequential)

    def test_save(self):
        filename = config.ml.brain.ancestor_example_name
        brain = BF.load(filename)
        files = os.listdir(self._dir)
        former_count = len(files)
        BF.save(brain)
        files = os.listdir(self._dir)
        latter_count = len(files)
        self.assertEqual(latter_count, former_count + 1)
        latest = BF.get_latest_filepath()
        os.unlink(latest)
