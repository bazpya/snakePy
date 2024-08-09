from tests.test_ import Test_
from unittest.mock import patch, call as Call
from src.ml.player import PlayerResult
from src.ml.evolution import Evolution
from src.ml.generation import GenerationResult
from src.config import config


class Evolution_(Test_):
    @patch("src.ml.evolution.Generation")  # !! point to the consuming code !!
    async def test_run_tells_about_ancestor_file_only_to_1st_gen(self, MockGeneration):
        config.ml.evolution.has_ancestor_file = True
        config.ml.evolution.generations = 2
        gen_count = config.ml.evolution.generations
        mock = MockGeneration.return_value
        run_result = GenerationResult(
            1, 0, [PlayerResult(player=None, fitness=0, game_res=None)]
        )
        mock.run.return_value = self.make_awaitable(run_result)
        sut = Evolution()
        await sut.run()
        self.assertEqual(MockGeneration.call_count, gen_count)
        self.assertEqual(
            MockGeneration.call_args_list[0],
            Call(0, None, True),
        )
        self.assertEqual(
            MockGeneration.call_args_list[1],
            Call(1, run_result, False),
        )
