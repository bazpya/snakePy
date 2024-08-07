from src.ml.brain_factory import BrainFactory
from tests.ml.test_ml_ import Test_ml_
import shutil


class Brain_(Test_ml_):
    def setUp(self) -> None:
        self.sut = BrainFactory.make(self.some, self.few)
        return super().setUp()

    def test_save_saves(self):
        path = "./models/bazdir"
        self.assertIsNotDir(path)
        self.sut.save(path)
        self.assertIsDir(path)
        shutil.rmtree(path)
        self.assertIsNotDir(path)
