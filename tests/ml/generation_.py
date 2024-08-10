from src.ml.generation import Generation
from src.config import config
from tests.testbase import Test_


class Generation_(Test_):

    def test_init_allows_previous_res_alone(self):
        etc = Generation(id=0, previous_res={})

    def test_init_allows_ancestor_file_alone(self):
        etc = Generation(id=0, has_ancestor_file=True)

    def test_init_rejects_previous_res_and_ancestor_file_together(self):
        self.assertRaises(
            ValueError,
            lambda: Generation(id=0, previous_res={}, has_ancestor_file=True),
        )

    selection_count_cases = [
        (False, 1, 0.999),
        (True, 1, 1),
        (True, 1, 1.001),
        (False, 3, 0.999 / 3),
    ]

    def test_rejects_selection_count_below_unit(self):
        for should_allow, population, selection_ratio in self.selection_count_cases:
            with self.subTest():
                config.ml.generation.population = population
                config.ml.evolution.selection_ratio = selection_ratio
                if should_allow:
                    etc = Generation(id=0)
                else:
                    self.assertRaises(ValueError, lambda: Generation(id=0))

    # baztodo
    def test_populate_spawns_correct_number_of_players(self): ...
