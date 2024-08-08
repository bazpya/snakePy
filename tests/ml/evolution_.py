from tests.test_ import Test_
from src.ml.evolution import Evolution
from src.config import config


class Evolution_(Test_):
    def test_specified_gen_count_uses_it(self):
        expected = self.few
        sut = Evolution(expected)
        actual = sut._gen_count
        self.assertEqual(actual, expected)

    def test_unspecified_gen_count_gets_from_config(self):
        config.ml.evolution.generations = self.many
        expected = config.ml.evolution.generations
        sut = Evolution(expected)
        actual = sut._gen_count
        self.assertEqual(actual, expected)
