from tests.testbase import Test_
from src.game.direction import Direction, Turn


class Direction_(Test_):
    def test_is_aligned_true(self):
        for sut, other in [
            (Direction.up, Direction.down),
            (Direction.right, Direction.left),
        ]:
            self.assertTrue(sut.is_aligned(other))
            self.assertTrue(other.is_aligned(sut))
            self.assertTrue(sut.is_aligned(sut))
            self.assertTrue(other.is_aligned(other))

    def test_is_aligned_false(self):
        for sut, other in [
            (Direction.up, Direction.left),
            (Direction.up, Direction.right),
            (Direction.down, Direction.left),
            (Direction.down, Direction.right),
        ]:
            self.assertFalse(sut.is_aligned(other))
            self.assertFalse(other.is_aligned(sut))

    def test_is_perpendicular_true(self):
        for sut, other in [
            (Direction.up, Direction.left),
            (Direction.up, Direction.right),
            (Direction.down, Direction.left),
            (Direction.down, Direction.right),
        ]:
            self.assertTrue(sut.is_perpendicular(other))
            self.assertTrue(other.is_perpendicular(sut))

    def test_is_perpendicular_false(self):
        for sut, other in [
            (Direction.up, Direction.down),
            (Direction.right, Direction.left),
        ]:
            self.assertFalse(sut.is_perpendicular(other))
            self.assertFalse(other.is_perpendicular(sut))
            self.assertFalse(sut.is_perpendicular(sut))
            self.assertFalse(other.is_perpendicular(other))

    def test_turns(self):
        for sut, other in [
            (Direction.up, Direction.right),
            (Direction.right, Direction.down),
            (Direction.down, Direction.left),
            (Direction.left, Direction.up),
        ]:
            self.assertEqual(sut.turn(Turn.right), other)
            self.assertEqual(other.turn(Turn.left), sut)
            self.assertEqual(sut.turn(Turn.ahead), sut)

    def test_any_returns_correct_type(self):
        sut = Direction.any()
        self.assertIsInstance(sut, Direction)
