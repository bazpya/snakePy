import tensorflow as tf
from src.ml.eye import Eye
from src.ml.view import View
from tests.ml.test_ml_ import Test_ml_


class Eye_(Test_ml_):
    def test_see_gets_tensor(self):
        view = View()
        sut = Eye(view)
        game = self.make_game()
        head = game.get_head()
        food = game._grid.get_random_blanks(1)[0]
        actual = sut.see(head, food)
        self.assertIsInstance(actual, tf.Tensor)

    def test_see_gets_the_right_shape(self):
        view = View(True, False, True, False, True)
        sut = Eye(view)
        game = self.make_game()
        head = game.get_head()
        food = game._grid.get_random_blanks(1)[0]
        actual = sut.see(head, food).shape
        self.assertEqual(actual, [view.size])
