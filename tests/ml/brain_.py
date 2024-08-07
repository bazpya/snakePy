from unittest import skip
from src.ml.brain_factory import BrainFactory
from tests.ml.test_ml_ import Test_ml_


class Brain_(Test_ml_):
    def setUp(self) -> None:
        self.sut = BrainFactory.make(self.some, self.few)
        return super().setUp()

    @skip("todo: Use bazpy to assert dump file")
    def test_save_saves(self):
        self.sut.save("./models/dasoos")
