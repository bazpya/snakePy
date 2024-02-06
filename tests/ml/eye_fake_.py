# import tensorflow as tf
# from src.ml.view import View
# from src.game.cell import Cell
# from src.ml.eye_fake import EyeFake
# from tests.ml.test_ml_ import Test_ml_


# class Eye_fake_see_(Test_ml_):
#     def test_see_gets_tensor(self):
#         view = View()
#         sut = EyeFake(view)
#         head = Cell()
#         food = Cell()
#         actual = sut.see(head, food)
#         self.assertIsInstance(actual, tf.Tensor)

#     def test_see_gets_the_right_shape(self):
#         view = View(True, False, True, False, True)
#         sut = EyeFake(view)
#         head = Cell()
#         food = Cell()
#         actual = sut.see(head, food).shape
#         self.assertEqual(actual, [view.size])

#     def test_see_gets_preset_output(self):
#         view = View(True, False, True, False, True)
#         sut = EyeFake(view)
#         head = Cell()
#         food = Cell()
#         expected = tf.random.normal([view.size])
#         sut.set_output(expected)
#         actual = sut.see(head, food)
#         self.assertTensorEqual(actual, expected)

#     def test_see_without_preset_output(self):
#         view = View(True, False, True, False, True)
#         sut = EyeFake(view)
#         head = Cell()
#         food = Cell()
#         expected = tf.random.normal([view.size])
#         actual = sut.see(head, food)
#         self.assertTensorDifferent(actual, expected)
