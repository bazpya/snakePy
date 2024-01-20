from ml.player import Player
from ml_test.player_ import Player_


class Player_init_(Player_):
    def test_init_makes_correct_number_of_layers(self):
        sut = self._get_sut()
        expected = len(self._model_params.layer_sizes) + 1
        actual = len(sut._model.layers)
        self.assertEqual(actual, expected)

    def test_init_makes_correct_layer_sizes(self):
        sut = self._get_sut()
        for i, size in enumerate(self._model_params.layer_sizes):
            layer = sut._model.layers[i]
            self.assertEqual(layer.units, size)

    def test_init_adds_correct_output_layer_size(self):
        sut = self._get_sut()
        last_layer = sut._model.layers[-1]
        output_layer_size = last_layer.units
        self.assertEqual(output_layer_size, Player._output_layer_size)
