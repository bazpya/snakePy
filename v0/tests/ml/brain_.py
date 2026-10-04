from tests.testbase import Test_
from src.ml.brain_factory import BrainFactory
import os


class Brain_(Test_):
    def setUp(self) -> None:
        self.sut = BrainFactory.make(self.some, self.few)
        return super().setUp()

    def test_save_saves(self):
        path = "./models/scratch_test.keras"
        self.assertIsNotFile(path)
        self.sut.save(path)
        self.assertIsFile(path)
        os.unlink(path)
        self.assertIsNotFile(path)
