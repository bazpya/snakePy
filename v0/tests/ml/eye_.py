from src.ml.ml import ML
from tests.testbase import Test_
from src.game.game import Game
from src.ml.eye import Eye
from src.ml.view import View


class Eye_(Test_):
    def test_see_gets_tensor(self):
        sut = Eye()
        game = Game()
        head = game.get_head()
        food = game._last_food
        actual = sut.see(head, food)
        self.assertIsInstance(actual, ML.Tensor)

    def test_see_gets_the_right_shape(self):
        view = View(True, False, True, False, True)
        sut = Eye(view)
        game = Game()
        head = game.get_head()
        food = game._last_food
        actual = sut.see(head, food).shape
        self.assertEqual(actual, [view.size])
