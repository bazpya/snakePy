from src.ml.brain import Brain
from src.ml_test.brain_ import Brain_


class Brain_init_(Brain_):
    def test_init_makes_correct_layer_sizes(self):
        sut = self._get_sut()
        for i, size in enumerate(self._model_params.layer_sizes):
            layer = sut._model.layers[i]
            self.assertEqual(layer.units, size)

    def test_init_adds_correct_output_layer_size(self):
        sut = self._get_sut()
        last_layer = sut._model.layers[-1]
        output_layer_size = last_layer.units
        self.assertEqual(output_layer_size, Brain._output_layer_size)
